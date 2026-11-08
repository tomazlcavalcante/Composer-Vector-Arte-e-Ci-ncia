"""F18 (rodada 3): interpolação Bach ↔ Debussy, v_t = (1−t)·v_Bach + t·v_Debussy (normalizado), alfa 0,75, semente neutra (Beethoven op. 27 n.º 2, ~10 s). Continuações para ESCUTA (ilustração, não experimento).

Mesma lógica de steering de F7 (camada 6, vetor centrado = centróide do alvo − média geral, norma = mediana
de ||h||, norma do estado preservada, top-p 0,98, máscara de tipo de token). Semente = as primeiras 50 notas
da peça; continuação de 120 notas. Cada grupo usa a MESMA semente de sorteio (torch.manual_seed) em todas as
condições; testa os sorteios 0, 1, 2, ... e fica com o primeiro em que nenhuma condição degenera (ok()).
Isso é seleção para escuta, não experimento: não usar para medir efeito.
Saída: MIDIs em escuta_midis/ e o sorteio usado em sorteios.txt.
Uso: CV_WINDOWS=1,2 python gerar.py [grupo ...]
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis" / "F0_infra"))
from analysis.common.emb import load, piece_level  # noqa: E402
from analysis.common.data import list_pieces  # noqa: E402

import torch  # noqa: E402
from transformers import AutoModelForCausalLM  # noqa: E402
from anticipation.convert import midi_to_events, events_to_midi  # noqa: E402
from anticipation.vocab import AUTOREGRESS, TIME_OFFSET, DUR_OFFSET, NOTE_OFFSET  # noqa: E402
from extract_amt import window  # noqa: E402

LAYER = 6
SEED_S, MAX_SEED, N_NEW = 10.5, 660, 360  # semente: tudo até 10,5 s (máx. 220 notas); 120 notas novas
OUT = HERE / "escuta3_midis"
OUT.mkdir(exist_ok=True)
torch.set_num_threads(2)

X, df = load(LAYER, "mean")
Xp, dp = piece_level(X, df)
gmean = Xp.mean(0)
hnorm = float(np.median(np.linalg.norm(Xp, axis=1)))


def centered(key):
    v = Xp[dp.composer_key.values == key].mean(0) - gmean
    return torch.tensor(v / np.linalg.norm(v) * hnorm, dtype=torch.float32)


r = np.random.default_rng(7).standard_normal(Xp.shape[1])
V = {
    "Chopin": centered("Chopin, Frédéric"),
    "Debussy": centered("Debussy, Claude"),
    "Bach": centered("Bach, Johann Sebastian"),
    "Mozart": centered("Mozart, Wolfgang Amadeus"),
    "Satie": centered("Satie, Erik"),
    "aleatorio": torch.tensor(r / np.linalg.norm(r) * hnorm, dtype=torch.float32),
}

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


def ok(seed, new):
    """Não degenerou: o tempo nunca volta, há pelo menos 40 ataques distintos nas 120 notas e a duração
    mediana é de pelo menos 30 ms."""
    t0 = max(seed[0::3])
    ts, ds = new[0::3], [d - DUR_OFFSET for d in new[1::3]]
    mono = all(b >= a for a, b in zip([t0] + ts[:-1], ts))
    return mono and len(set(ts)) >= 40 and sorted(ds)[len(ds) // 2] >= 3


pieces = list_pieces("/home/claude/data/giant/surname_checked_midis")
from anticipation import ops  # noqa: E402
from analysis.common.emb import center, l2norm  # noqa: E402

Xc, mu = center(Xp)
Z = l2norm(Xc)
A = Z[dp.composer_key.values == "Bach, Johann Sebastian"].mean(0)
B = Z[dp.composer_key.values == "Debussy, Claude"].mean(0)


@torch.no_grad()
def reread(new):
    seq = ops.translate(new, -ops.min_time(new, seconds=False), seconds=False)
    hs = model(torch.tensor([[AUTOREGRESS] + seq]), output_hidden_states=True).hidden_states[LAYER][0]
    z = l2norm((hs[1:].mean(0).numpy() - mu)[None])[0]
    d = B - A
    return float(np.dot(z - A, d) / np.dot(d, d))


def seed_of(surname, title):
    p = next(p for p in pieces if p.surname == surname and p.title == title)
    ev = window(midi_to_events(str(p.path)), 0.0)
    keep = [i for i in range(0, len(ev), 3) if ev[i] < SEED_S * 100][: MAX_SEED // 3]
    return [t for i in keep for t in ev[i:i + 3]]


def mix(t):
    v = (1 - t) * V["Bach"] + t * V["Debussy"]
    return v / v.norm() * hnorm


ALFA = 0.75
CONDS = [("1_sem_vetor", None)] + [(f"2_t{int(t * 100):03d}", t) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
seed = seed_of("Beethoven", "Piano Sonata No.14, Op.27 No.2")
events_to_midi(seed).save(str(OUT / "i_0_semente_beethoven.mid"))
print("semente: %d notas, termina em %.1f s" % (len(seed) // 3, max(seed[0::3]) / 100), flush=True)


def run(t, rs):
    torch.manual_seed(rs)
    state["v"], state["a"] = (None, 0.0) if t is None else (mix(t), ALFA)
    new = gen(seed, N_NEW)
    state["v"], state["a"] = None, 0.0
    return new


chosen = None
for rs in range(4):
    outs = {}
    for name, t in CONDS:
        new = run(t, rs)
        if not ok(seed, new):
            print("  degenerou:", name, "sorteio", rs, flush=True)
            break
        outs[name] = (rs, new)
    if len(outs) == len(CONDS):
        chosen = outs
        break
if chosen is None:
    chosen = {}
    for name, t in CONDS:
        for rs in range(4, 12):
            new = run(t, rs)
            if ok(seed, new):
                chosen[name] = (rs, new)
                break
            print("  degenerou:", name, "sorteio", rs, flush=True)
log = []
for name, t in CONDS:
    if name in chosen:
        rs, new = chosen[name]
        events_to_midi(seed + new).save(str(OUT / f"i_{name}.mid"))
        p = reread(new)
        log.append(f"{name}\tsorteio {rs}\tposição no eixo Bach→Debussy {p:.3f}")
    else:
        log.append(f"{name}\tfalhou")
    print(log[-1], flush=True)
(HERE / "sorteios3.txt").write_text("\n".join(log) + "\n")
