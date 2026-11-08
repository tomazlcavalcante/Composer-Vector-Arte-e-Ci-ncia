"""F18: continuações para ESCUTA (ilustração, não experimento).

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
N_SEED, N_NEW = 150, 360  # 50 notas de semente, 120 notas novas
OUT = HERE / "escuta_midis"
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
    "Joplin": centered("Joplin, Scott"),
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


def seed_of(surname, title):
    p = next(p for p in pieces if p.surname == surname and p.title == title)
    return window(midi_to_events(str(p.path)), 0.0)[:N_SEED]  # frac 0 = começo da peça


SEEDS = {
    "bach": ("Bach", "Invention in A minor, BWV 784"),
    "mozart": ("Mozart", "Piano Sonata No.11 in A major, K.331_300i"),
    "chopin": ("Chopin", "Nocturne in E minor, Op.72 No.1"),
    "odeon": ("Nazareth", "Odeon"),
    "ticotico": ("Abreu", "Tico-Tico no fubá"),
}
GROUPS = [  # (semente, [(arquivo, vetor, alfa), ...])
    ("bach", [("01_bach_sem_vetor", None, 0.0), ("02_bach_chopin_a1", "Chopin", 1.0),
              ("03_bach_chopin_a2", "Chopin", 2.0), ("04_bach_aleatorio_a1_5", "aleatorio", 1.5)]),
    ("mozart", [("05_mozart_sem_vetor", None, 0.0), ("06_mozart_debussy_a1", "Debussy", 1.0)]),
    ("chopin", [("07_chopin_sem_vetor", None, 0.0), ("08_chopin_joplin_a1", "Joplin", 1.0)]),
    ("odeon", [("09_odeon_sem_vetor", None, 0.0), ("10_odeon_chopin_a1_5", "Chopin", 1.5)]),
    ("ticotico", [("11_ticotico_sem_vetor", None, 0.0), ("12_ticotico_satie_a0_6", "Satie", 0.6)]),
]

only = sys.argv[1:]
seeds = {k: seed_of(*v) for k, v in SEEDS.items() if not only or k in only}
log = []
for k, s in seeds.items():
    events_to_midi(s).save(str(OUT / f"00_semente_{k}.mid"))
    print(k, "semente termina em %.1f s" % (max(s[0::3]) / 100), flush=True)

for sk, conds in GROUPS:
    if sk not in seeds:
        continue
    for rs in range(8):
        outs, good = {}, True
        for name, vk, a in conds:
            torch.manual_seed(rs)
            state["v"], state["a"] = (V[vk] if vk else None), a
            new = gen(seeds[sk], N_NEW)
            state["v"], state["a"] = None, 0.0
            if not ok(seeds[sk], new):
                good = False
                print("  degenerou:", name, "sorteio", rs, flush=True)
                break
            outs[name] = new
        if good:
            for name, new in outs.items():
                events_to_midi(seeds[sk] + new).save(str(OUT / f"{name}.mid"))
            print("ok", sk, "sorteio", rs, flush=True)
            log.append(f"{sk}\tsorteio {rs}")
            break
    else:
        print("FALHOU", sk, flush=True)
        log.append(f"{sk}\tfalhou")
(HERE / f"sorteios_{'_'.join(only) or 'todos'}.txt").write_text("\n".join(log) + "\n")
