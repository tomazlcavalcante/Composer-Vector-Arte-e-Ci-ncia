"""F7: MIDIs de exemplo para a apresentação (ilustração, não experimento).

Reaproveita a lógica de run.py (parte b): semente de 150 tokens (50 notas) de UMA peça de Bach (a primeira
da lista sorteada por run.py com random_state=1), continuação de 240 tokens (80 notas), condições
sem steering / centrado de Chopin com alpha = 1 / alpha = 1,5. Semente de geração fixa: torch.manual_seed(0)
antes de cada condição. Não altera run.py nem CSVs/metrics.
Uso: CV_WINDOWS=1,2 python exemplos_midi.py
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "F0_infra"))
from analysis.common.emb import load, piece_level  # noqa: E402
from analysis.common.data import list_pieces  # noqa: E402

import torch  # noqa: E402
import mido  # noqa: E402
from transformers import AutoModelForCausalLM  # noqa: E402
from anticipation.convert import midi_to_events, events_to_midi  # noqa: E402
from anticipation.vocab import AUTOREGRESS, TIME_OFFSET, DUR_OFFSET, NOTE_OFFSET  # noqa: E402
from extract_amt import window  # noqa: E402

SRC, TGT = "Bach, Johann Sebastian", "Chopin, Frédéric"
N_SEED, N_NEW = 150, 240
OUT = HERE / "exemplos_midi"
OUT.mkdir(exist_ok=True)

cfg = json.loads((HERE.parent / "F2_representacao" / "metrics.json").read_text())["best"]
LAYER, POOL = cfg["layer"], cfg["pooling"]
X, df = load(LAYER, POOL)
Xp, dp = piece_level(X, df)

model = AutoModelForCausalLM.from_pretrained("/home/claude/models/music-small-800k").eval()
block = model.transformer.h[LAYER - 1]
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
gmean = Xp.mean(0)
hnorm = float(np.median(np.linalg.norm(Xp, axis=1)))
v = Xp[dp.composer_key.values == TGT].mean(0) - gmean
v = v / np.linalg.norm(v) * hnorm
V_CHOPIN = torch.tensor(v, dtype=torch.float32)


def allowed(pos):
    return [(TIME_OFFSET, DUR_OFFSET), (DUR_OFFSET, NOTE_OFFSET), (NOTE_OFFSET, NOTE_OFFSET + 128)][pos % 3]


@torch.no_grad()
def gen(seed, n_new):
    x = torch.tensor([[AUTOREGRESS] + seed])
    o = model(x, use_cache=True)
    past, logits = o.past_key_values, o.logits[0, -1]
    new = []
    for i in range(n_new):
        lo, hi = allowed(len(seed) + i)
        mask = torch.full_like(logits, float("-inf"))
        mask[lo:hi] = 0
        p = torch.softmax(logits + mask, -1)
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


paths = {p.piece_id: p.path for p in list_pieces("/home/claude/data/giant/surname_checked_midis")}
ids = dp[dp.composer_key == SRC].sample(4, random_state=1).piece_id.tolist()  # default n_seeds=4 de run.py
seed = None
for sid in ids:
    ev = window(midi_to_events(str(paths[sid])), 0.5)
    if ev is not None:
        seed = ev[:N_SEED]
        break
print("peça:", sid, paths[sid], flush=True)


def save(tokens, name):
    events_to_midi(tokens).save(str(OUT / name))


save(seed, "semente.mid")
conds = [("sem_steering.mid", None, 0.0), ("chopin_alfa1.mid", V_CHOPIN, 1.0), ("chopin_alfa1_5.mid", V_CHOPIN, 1.5)]
for name, vec, a in conds:
    torch.manual_seed(0)
    state["v"], state["a"] = vec, a
    new = gen(seed, N_NEW)
    state["v"], state["a"] = None, 0.0
    save(seed + new, name)  # tempos absolutos: sem relativizar
    print("ok", name, flush=True)

(OUT / "peca.txt").write_text(f"{sid}\n{paths[sid]}\n")
for f in ["semente.mid", *[c[0] for c in conds]]:
    m = mido.MidiFile(str(OUT / f))
    n = sum(1 for t in m.tracks for msg in t if msg.type == "note_on" and msg.velocity > 0)
    print(f, "notas:", n, "duração (s): %.2f" % m.length)
