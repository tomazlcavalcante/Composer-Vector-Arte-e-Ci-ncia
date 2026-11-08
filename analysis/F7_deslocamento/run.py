"""F7: deslocamento (Q4, hipóteses H6 e H7).

(a) Geométrico, sem geração: para o segmento J. S. Bach -> Chopin entre os centróides, a distância de cada
    outro compositor ao segmento e o parâmetro t da projeção; comparado a um nulo (posições dos mesmos
    compositores com rótulos de peças permutados não fazem sentido aqui, então usamos a distribuição das
    distâncias de todos os compositores ao segmento e reportamos os mais próximos e seus t).
(b) Piloto de steering: semente = janela do meio de peças do compositor de origem; gera N tokens com o
    vetor somado na camada escolhida (forma do artigo: h <- (h + a v)|h|/|h + a v| em todas as posições),
    condições {nenhum, aleatório de mesma norma, centrado (alvo - média geral)} x alpha; a continuação é
    RELIDA SEM steering e projetada na direção origem->alvo (0 = origem, 1 = alvo).
    Caminho Bach->Chopin: vetor (1 - t) v_Bach + t v_Chopin (centrados), t em {0, 0,5, 1}.
Uso: python run.py --part a|b [--n-seeds 4 --new 150]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "F0_infra"))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--part", default="a")
ap.add_argument("--n-seeds", type=int, default=4)
ap.add_argument("--new", type=int, default=150)
ap.add_argument("--src", default="Bach, Johann Sebastian")
ap.add_argument("--tgt", default="Chopin, Frédéric")
ap.add_argument("--set", default="piloto", choices=["piloto", "forte", "alfa"])
ap.add_argument("--reps", type=int, default=2)
args = ap.parse_args()
cfg = json.loads((HERE.parent / "F2_representacao" / "metrics.json").read_text())["best"]
LAYER, POOL = cfg["layer"], cfg["pooling"]
rng = np.random.default_rng(0)
(HERE / "figs").mkdir(exist_ok=True)

X, df = load(LAYER, POOL)
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp)
Z = l2norm(Xc)
C, keys = centroids(Z, dp)
ia, ib = keys.index(args.src), keys.index(args.tgt)
A, Bv = C[ia], C[ib]
metrics_path = HERE / "metrics.json"
out = json.loads(metrics_path.read_text()) if metrics_path.exists() else {}
out.update(layer=LAYER, pooling=POOL)

if args.part == "a":
    meta = load_meta().set_index("composer_key")
    d = Bv - A
    rows = []
    for i, k in enumerate(keys):
        if i in (ia, ib):
            continue
        t = float(np.dot(C[i] - A, d) / np.dot(d, d))
        tc = min(max(t, 0), 1)
        dist = float(np.linalg.norm(C[i] - (A + tc * d)))
        rows.append(dict(composer=k, t=round(t, 3), dist_ao_segmento=round(dist, 4), birth=meta.loc[k, "birth"],
                         periodo=meta.loc[k, "periodo"]))
    seg = pd.DataFrame(rows).sort_values("dist_ao_segmento")
    seg.to_csv(HERE / "caminho_bach_chopin.csv", index=False)
    from scipy.stats import spearmanr
    inside = seg[(seg.t > 0) & (seg.t < 1)]
    out["a_caminho"] = dict(
        mais_proximos_do_segmento=seg.head(8)[["composer", "t", "dist_ao_segmento", "periodo"]].to_dict("records"),
        rho_t_vs_nascimento_dentro_do_segmento=round(float(spearmanr(inside.t, inside.birth).statistic), 3) if len(inside) > 3 else None,
        dist_bach_chopin=round(float(np.linalg.norm(d)), 4))
else:
    import torch
    from transformers import AutoModelForCausalLM
    from anticipation.convert import midi_to_events
    from anticipation.vocab import AUTOREGRESS, TIME_OFFSET, DUR_OFFSET, NOTE_OFFSET
    from extract_amt import window
    from analysis.common.data import list_pieces

    torch.manual_seed(0)
    model = AutoModelForCausalLM.from_pretrained("/home/claude/models/music-small-800k").eval()
    block = model.transformer.h[LAYER - 1] if LAYER >= 1 else None
    state = {"v": None, "a": 0.0}

    def hook(mod, inp, outp):
        if state["v"] is None or state["a"] == 0:
            return outp
        h = outp[0] if isinstance(outp, tuple) else outp
        n0 = h.norm(dim=-1, keepdim=True)
        hs = h + state["a"] * state["v"]
        hs = hs * n0 / (hs.norm(dim=-1, keepdim=True) + 1e-8)
        return (hs,) + tuple(outp[1:]) if isinstance(outp, tuple) else hs

    block.register_forward_hook(hook)
    # vetores no espaço bruto da camada (o hook atua no estado bruto): centrado = centróide bruto do alvo - média geral
    raw_cent = {k: Xp[dp.composer_key.values == k].mean(0) for k in keys}
    gmean = Xp.mean(0)
    hnorm = float(np.median(np.linalg.norm(Xp, axis=1)))

    def vec(kind, k=None, t=None):
        if kind == "centrado":
            v = raw_cent[k] - gmean
        elif kind == "caminho":
            v = (1 - t) * (raw_cent[args.src] - gmean) + t * (raw_cent[args.tgt] - gmean)
        else:
            v = rng.standard_normal(768)
        v = v / np.linalg.norm(v) * hnorm  # mesma norma para todas as condições; alpha relativo a |h|
        return torch.tensor(v, dtype=torch.float32)

    def allowed(pos):
        return [(TIME_OFFSET, DUR_OFFSET), (DUR_OFFSET, NOTE_OFFSET), (NOTE_OFFSET, NOTE_OFFSET + 128)][pos % 3]

    @torch.no_grad()
    def gen(seed, n_new):
        ids = [AUTOREGRESS] + seed
        x = torch.tensor([ids])
        o = model(x, use_cache=True)
        past, logits = o.past_key_values, o.logits[0, -1]
        new = []
        for i in range(n_new):
            lo, hi = allowed(len(seed) + i)
            mask = torch.full_like(logits, float("-inf"))
            mask[lo:hi] = 0
            p = torch.softmax((logits + mask) / 1.0, -1)
            p_sorted, idx = torch.sort(p, descending=True)
            keep = torch.cumsum(p_sorted, 0) <= 0.98
            keep[0] = True
            p2 = torch.zeros_like(p)
            p2[idx[keep]] = p_sorted[keep]
            tok = int(torch.multinomial(p2 / p2.sum(), 1))
            new.append(tok)
            o = model(torch.tensor([[tok]]), past_key_values=past, use_cache=True)
            past, logits = o.past_key_values, o.logits[0, -1]
        return new

    @torch.no_grad()
    def reread(tokens):
        state["a"] = 0.0
        x = torch.tensor([[AUTOREGRESS] + tokens])
        hs = model(x, output_hidden_states=True).hidden_states[LAYER][0]
        v = (hs[1:].mean(0) if POOL == "mean" else hs[-1]).numpy()
        return l2norm((v - mu)[None])[0]

    def progress(z):
        d = Bv - A
        return float(np.dot(z - A, d) / np.dot(d, d))

    paths = {p.piece_id: p.path for p in list_pieces("/home/claude/data/giant/surname_checked_midis")}
    seeds_ids = dp[dp.composer_key == args.src].sample(args.n_seeds, random_state=1).piece_id.tolist()
    if args.set == "piloto":
        conds = [("nenhum", None, 0.0, None), ("aleatorio", "aleatorio", 0.5, None), ("centrado", "centrado", 0.2, None),
                 ("centrado", "centrado", 0.5, None), ("centrado", "centrado", 1.0, None),
                 ("caminho_t0.5", "caminho", 0.5, 0.5)]
    elif args.set == "alfa":  # varredura de intensidade: centrado vs aleatório
        conds = [("nenhum", None, 0.0, None)] + [(n, n, a, None) for a in (0.25, 0.5, 1.0, 1.5)
                                                  for n in ("centrado", "aleatorio")]
    else:  # controles com a mesma intensidade (alpha = 1) e caminho Bach -> Chopin
        conds = [("nenhum", None, 0.0, None), ("aleatorio", "aleatorio", 1.0, None), ("centrado", "centrado", 1.0, None),
                 ("caminho_t0", "caminho", 1.0, 0.0), ("caminho_t0.5", "caminho", 1.0, 0.5), ("caminho_t1", "caminho", 1.0, 1.0)]
    rows = []
    for sid in seeds_ids:
        ev = window(midi_to_events(str(paths[sid])), 0.5)
        if ev is None:
            continue
        seed = ev[:150]  # 50 eventos de semente
        for name, kind, a, tt in conds:
            for rep in range(args.reps):
                state["v"] = vec(kind, args.tgt, tt) if kind else None
                state["a"] = a
                new = gen(seed, args.new)
                state["a"] = 0.0
                # relê só a continuação (tempo relativizado ao seu início)
                from anticipation import ops
                cont = ops.translate(new, -ops.min_time(new, seconds=False), seconds=False)
                z = reread(cont)
                notes = [(t - NOTE_OFFSET) % 128 for t in new[2::3]]
                rep_rate = 1 - len(set(zip(notes, notes[1:], notes[2:]))) / max(1, len(notes) - 2)
                rows.append(dict(seed=sid, cond=name, alpha=a, rep=rep, progresso=progress(z),
                                 dist_alvo=float(cosine_dist(z[None], Bv[None])[0, 0]),
                                 dist_origem=float(cosine_dist(z[None], A[None])[0, 0]), repeticao_trigramas=rep_rate))
                print(rows[-1], flush=True)
    res = pd.DataFrame(rows)
    tag = args.set + ("" if args.src.startswith("Bach") and args.tgt.startswith("Chopin") else "_" + args.src.split(",")[0] + "_" + args.tgt.split(",")[0])
    res.to_csv(HERE / f"steering_{tag}.csv", index=False)
    summ = res.groupby(["cond", "alpha"]).agg(progresso=("progresso", "mean"), progresso_dp=("progresso", "std"),
                                              repeticao=("repeticao_trigramas", "mean"), n=("progresso", "size")).round(3)
    out[f"b_{tag}"] = dict(origem=args.src, alvo=args.tgt, n_novos_tokens=args.new,
                           resumo=summ.reset_index().to_dict("records"))
    print(summ)

metrics_path.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in out.items() if not k.startswith("b_")}, indent=1, ensure_ascii=False))
