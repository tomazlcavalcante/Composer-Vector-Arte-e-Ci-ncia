"""F18 (rodada 2): peças famosas, semente de pelo menos 10 s, alfa de 0,5 a 1. Continuações para ESCUTA (ilustração, não experimento).

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
OUT = HERE / "escuta2_midis"
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


def seed_of(surname, title):
    p = next(p for p in pieces if p.surname == surname and p.title == title)
    ev = window(midi_to_events(str(p.path)), 0.0)  # começo da peça, tempo relativo
    keep = [i for i in range(0, len(ev), 3) if ev[i] < SEED_S * 100][: MAX_SEED // 3]
    return [t for i in keep for t in ev[i:i + 3]]


SEEDS = {
    "bach": ("Bach", "Prelude and Fugue in C major, BWV 846"),
    "elise": ("Beethoven", "Für Elise, WoO 59"),
    "gymnopedie": ("Satie", "3 Gymnopédies"),
    "mozart545": ("Mozart", "Piano Sonata No.16 in C major, K.545"),
    "impromptu": ("Chopin", "Fantaisie-impromptu, Op.66"),
}
ALFAS = [0.0, 0.5, 0.75, 1.0]
GROUPS = [("bach", "Chopin"), ("elise", "Debussy"), ("gymnopedie", "Bach"), ("mozart545", "Satie"),
          ("impromptu", "Mozart")]


def run(seed, vk, a, rs):
    torch.manual_seed(rs)
    state["v"], state["a"] = (V[vk] if a else None), a
    new = gen(seed, N_NEW)
    state["v"], state["a"] = None, 0.0
    return new


only = sys.argv[1:]
log = []
for i, (sk, vk) in enumerate(GROUPS, 1):
    if only and sk not in only:
        continue
    seed = seed_of(*SEEDS[sk])
    t_end = max(seed[0::3]) / 100
    events_to_midi(seed).save(str(OUT / f"g{i}_{sk}_0_semente.mid"))
    print(sk, "semente: %d notas, termina em %.1f s" % (len(seed) // 3, t_end), flush=True)
    log.append(f"{sk}\tsemente {len(seed) // 3} notas, {t_end:.1f} s")
    # 1º: o mesmo sorteio para as 4 condições (até 4 tentativas); senão, sorteio próprio por condição
    chosen = None
    for rs in range(4):
        outs = {}
        for a in ALFAS:
            new = run(seed, vk, a, rs)
            if not ok(seed, new):
                print("  degenerou: alfa", a, "sorteio", rs, flush=True)
                break
            outs[a] = new
        if len(outs) == len(ALFAS):
            chosen = {a: (rs, n) for a, n in outs.items()}
            break
    if chosen is None:
        chosen = {}
        for a in ALFAS:
            for rs in range(4, 12):
                new = run(seed, vk, a, rs)
                if ok(seed, new):
                    chosen[a] = (rs, new)
                    break
                print("  degenerou: alfa", a, "sorteio", rs, flush=True)
    for a in ALFAS:
        tag = "1_sem_vetor" if a == 0 else f"2_{vk.lower()}_a{str(a).replace('.', '_')}"
        if a in chosen:
            rs, new = chosen[a]
            events_to_midi(seed + new).save(str(OUT / f"g{i}_{sk}_{tag}.mid"))
            log.append(f"{sk}\talfa {a}\tsorteio {rs}")
        else:
            log.append(f"{sk}\talfa {a}\tfalhou")
    print("ok", sk, {a: c[0] for a, c in chosen.items()}, flush=True)
(HERE / f"sorteios2_{'_'.join(only) or 'todos'}.txt").write_text("\n".join(log) + "\n")
