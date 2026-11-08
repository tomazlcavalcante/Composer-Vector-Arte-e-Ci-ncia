"""F7: descritores simbólicos independentes do modelo (PLANO, princípio 7).

Descritores sobre tokens de eventos do AMT (triplas tempo, duração, nota; passos de 10 ms):
notas/s, altura média, desvio da altura, extensão (p95-p5), duração média (s), polifonia média (grade de 50 ms).
1) referência: janela do meio (fração 0,5) de todas as peças de Bach e de Chopin;
2) experimento: continuação gerada (lógica de run.py --set forte) nas condições nenhum, aleatório α=1, centrado Chopin α=1;
3) comparação pareada por semente (média das amostras), Wilcoxon e nº de sementes na direção de Chopin.
Uso: CV_WINDOWS=1,2 python descritores.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "F0_infra"))
from analysis.common.emb import load, piece_level  # noqa: E402
from analysis.common.data import list_pieces  # noqa: E402
from anticipation import ops  # noqa: E402
from anticipation.convert import midi_to_events  # noqa: E402
from anticipation.vocab import AUTOREGRESS, TIME_OFFSET, DUR_OFFSET, NOTE_OFFSET  # noqa: E402
from extract_amt import window  # noqa: E402

SRC, TGT = "Bach, Johann Sebastian", "Chopin, Frédéric"
NEW, NSEED, REPS, ALPHA = 120, 7, 2, 1.0
DESC = ["notas_por_s", "altura_media", "altura_dp", "extensao_p95_p5", "dur_media_s", "polifonia_media"]


def descritores(tokens):
    """tokens: lista de eventos (múltiplo de 3), tempo relativo ao início."""
    n = len(tokens) // 3
    if n < 3:
        return {k: np.nan for k in DESC}
    t = np.array(tokens[0:3 * n:3], float) - TIME_OFFSET
    d = np.array(tokens[1:3 * n:3], float) - DUR_OFFSET
    p = (np.array(tokens[2:3 * n:3]) - NOTE_OFFSET) % 128
    on, off = t * 0.01, (t + d) * 0.01
    t0, t1 = on.min(), off.max()
    span = max(t1 - t0, 1e-6)
    grid = np.arange(t0, t1, 0.05)
    poly = ((on[None, :] <= grid[:, None]) & (grid[:, None] < off[None, :])).sum(1).mean() if len(grid) else np.nan
    return dict(notas_por_s=n / span, altura_media=p.mean(), altura_dp=p.std(),
                extensao_p95_p5=np.percentile(p, 95) - np.percentile(p, 5), dur_media_s=(d * 0.01).mean(),
                polifonia_media=poly)


# ---------------- referência ----------------
pieces = [p for p in list_pieces("/home/claude/data/giant/surname_checked_midis") if p.composer_key in (SRC, TGT)]
rows = []
for p in pieces:
    try:
        ev = window(midi_to_events(str(p.path)), 0.5)
    except Exception as e:  # noqa: BLE001
        print("erro", p.piece_id, e, flush=True)
        continue
    if ev is None:
        continue
    rows.append(dict(piece_id=p.piece_id, composer=p.composer_key, **descritores(ev)))
ref = pd.DataFrame(rows)
ref.to_csv(HERE / "descritores_ref.csv", index=False)
refsum = {c: {d: dict(media=float(g[d].mean()), dp=float(g[d].std()), n=int(g[d].notna().sum())) for d in DESC}
          for c, g in ref.groupby("composer")}
print(json.dumps(refsum, indent=1, ensure_ascii=False), flush=True)
direcao = {d: float(np.sign(refsum[TGT][d]["media"] - refsum[SRC][d]["media"])) for d in DESC}

# ---------------- geração (cópia mínima de run.py) ----------------
import torch  # noqa: E402
from transformers import AutoModelForCausalLM  # noqa: E402

cfg = json.loads((HERE.parent / "F2_representacao" / "metrics.json").read_text())["best"]
LAYER = cfg["layer"]
X, df = load(LAYER, cfg["pooling"])
Xp, dp = piece_level(X, df)
gmean = Xp.mean(0)
hnorm = float(np.median(np.linalg.norm(Xp, axis=1)))
raw_t = Xp[dp.composer_key.values == TGT].mean(0)

torch.manual_seed(0)
rng = np.random.default_rng(0)
model = AutoModelForCausalLM.from_pretrained("/home/claude/models/music-small-800k").eval()
state = {"v": None, "a": 0.0}


def hook(mod, inp, outp):
    if state["v"] is None or state["a"] == 0:
        return outp
    h = outp[0] if isinstance(outp, tuple) else outp
    n0 = h.norm(dim=-1, keepdim=True)
    hs = h + state["a"] * state["v"]
    hs = hs * n0 / (hs.norm(dim=-1, keepdim=True) + 1e-8)
    return (hs,) + tuple(outp[1:]) if isinstance(outp, tuple) else hs


model.transformer.h[LAYER - 1].register_forward_hook(hook)


def vec(kind):
    v = (raw_t - gmean) if kind == "centrado" else rng.standard_normal(768)
    return torch.tensor(v / np.linalg.norm(v) * hnorm, dtype=torch.float32)


def allowed(pos):
    return [(TIME_OFFSET, DUR_OFFSET), (DUR_OFFSET, NOTE_OFFSET), (NOTE_OFFSET, NOTE_OFFSET + 128)][pos % 3]


@torch.no_grad()
def gen(seed, n_new):
    o = model(torch.tensor([[AUTOREGRESS] + seed]), use_cache=True)
    past, logits = o.past_key_values, o.logits[0, -1]
    new = []
    for i in range(n_new):
        lo, hi = allowed(len(seed) + i)
        mask = torch.full_like(logits, float("-inf"))
        mask[lo:hi] = 0
        p = torch.softmax(logits + mask, -1)
        ps, idx = torch.sort(p, descending=True)
        keep = torch.cumsum(ps, 0) <= 0.98
        keep[0] = True
        p2 = torch.zeros_like(p)
        p2[idx[keep]] = ps[keep]
        tok = int(torch.multinomial(p2 / p2.sum(), 1))
        new.append(tok)
        o = model(torch.tensor([[tok]]), past_key_values=past, use_cache=True)
        past, logits = o.past_key_values, o.logits[0, -1]
    return new


paths = {p.piece_id: p.path for p in list_pieces("/home/claude/data/giant/surname_checked_midis")}
seeds_ids = dp[dp.composer_key == SRC].sample(NSEED, random_state=1).piece_id.tolist()
conds = [("nenhum", None, 0.0), ("aleatorio", "aleatorio", ALPHA), ("centrado", "centrado", ALPHA)]
rows = []
for sid in seeds_ids:
    ev = window(midi_to_events(str(paths[sid])), 0.5)
    if ev is None:
        continue
    seed = ev[:150]
    for name, kind, a in conds:
        for rep in range(REPS):
            state["v"] = vec(kind) if kind else None
            state["a"] = a
            new = gen(seed, NEW)
            state["a"] = 0.0
            cont = ops.translate(new, -ops.min_time(new, seconds=False), seconds=False)
            rows.append(dict(seed=sid, cond=name, rep=rep, **descritores(cont)))
            print(rows[-1], flush=True)
st = pd.DataFrame(rows)
st.to_csv(HERE / "descritores_steering.csv", index=False)

# ---------------- comparações pareadas ----------------
m = st.groupby(["seed", "cond"])[DESC].mean().reset_index()
res = {}
for d in DESC:
    w = m.pivot(index="seed", columns="cond", values=d).dropna()
    r = dict(bach_ref=refsum[SRC][d], chopin_ref=refsum[TGT][d], direcao_chopin=direcao[d], n_sementes=len(w),
             media_cond={c: float(w[c].mean()) for c in w.columns})
    for nome, base in (("centrado_menos_nenhum", "nenhum"), ("centrado_menos_aleatorio", "aleatorio")):
        diff = (w["centrado"] - w[base]).values
        try:
            pv = float(wilcoxon(diff).pvalue)
        except ValueError:
            pv = float("nan")
        r[nome] = dict(diff_media=float(diff.mean()), sementes_na_direcao_chopin=int((diff * direcao[d] > 0).sum()),
                       sementes_contra=int((diff * direcao[d] < 0).sum()), wilcoxon_p=pv)
    res[d] = r
(HERE / "metrics_descritores.json").write_text(json.dumps(dict(config=dict(camada=LAYER, alpha=ALPHA, novos=NEW, reps=REPS, n_sementes=NSEED),
                                                           referencia=refsum, steering=res), indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))
