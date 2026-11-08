"""F0 (versão AMT): extrai representações do Anticipatory Music Transformer small
(stanford-crfm/music-small-800k) para as peças dos compositores selecionados.

Formato de entrada igual ao do treino do AMT no modo autoregressivo:
[AUTOREGRESS] + até 341 eventos (tempo, duração, nota), com tempo relativo ao início da janela
e janela limitada a 100 s.

Passes (retomáveis): pass 1 = janela do meio de cada peça; passes 2 e 3 = janelas a 1/6 e 5/6.
Saída: um .npz por (peça, janela) em $CV_EMBEDDINGS/amt/, com
  last[13, 768], mean[13, 768] (float16; índice 0 = embeddings, 1..12 = blocos), loss, n_tokens.

Uso: python extract_amt.py --pass 1 --budget-min 9
"""
import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.common.data import list_pieces  # noqa: E402

from anticipation import ops  # noqa: E402
from anticipation.convert import midi_to_events  # noqa: E402
from anticipation.vocab import AUTOREGRESS  # noqa: E402
from transformers import AutoModelForCausalLM  # noqa: E402

MAX_TIME_BINS = 100 * 100  # 100 s com resolução de 10 ms
N_EVENTS = 341
FRACTIONS = {1: 0.5, 2: 1 / 6, 3: 5 / 6}
EXTRA_PIECES = ["Abreu, Zequinha, Tico-Tico no fubá"]  # exemplo ilustrativo


def window(events, frac):
    n_ev = len(events) // 3
    if n_ev < 60:
        return None
    start_ev = max(0, min(n_ev - N_EVENTS, int(frac * n_ev) - N_EVENTS // 2))
    seq = events[3 * start_ev: 3 * (start_ev + N_EVENTS)]
    seq = ops.translate(seq, -ops.min_time(seq, seconds=False), seconds=False)
    # corta eventos além de 100 s (fora do vocabulário de tempo)
    keep = [i for i in range(0, len(seq), 3) if seq[i] - 0 < MAX_TIME_BINS]
    seq = [t for i in keep for t in seq[i:i + 3]]
    return seq if len(seq) >= 180 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pass", dest="p", type=int, default=1)
    ap.add_argument("--budget-min", type=float, default=9.0)
    ap.add_argument("--midis", default=os.environ.get("CV_MIDIS", "/home/claude/data/giant/surname_checked_midis"))
    ap.add_argument("--model", default=os.environ.get("CV_AMT", "/home/claude/models/music-small-800k"))
    ap.add_argument("--out", default=os.environ.get("CV_EMBEDDINGS", "/home/claude/data/embeddings"))
    args = ap.parse_args()
    torch.set_num_threads(os.cpu_count())

    meta = pd.read_csv(ROOT / "analysis" / "data" / "metadata_curated.csv")
    keys = set(meta.loc[meta.incluir == 1, "composer_key"])
    pieces = [p for p in list_pieces(args.midis)
              if p.composer_key in keys or any(p.piece_id.startswith(e) for e in EXTRA_PIECES)]
    out = Path(args.out) / "amt"
    out.mkdir(parents=True, exist_ok=True)
    todo = [p for p in pieces if not (out / f"{p.piece_id}__w{args.p}.npz").exists()
            and not (out / f"{p.piece_id}__w{args.p}.skip").exists()]
    print(f"pass {args.p}: {len(pieces)} peças, faltam {len(todo)}", flush=True)

    model = AutoModelForCausalLM.from_pretrained(args.model).eval()
    t0, done = time.time(), 0
    for p in todo:
        if time.time() - t0 > args.budget_min * 60:
            break
        try:
            seq = window(midi_to_events(str(p.path)), FRACTIONS[args.p])
        except Exception as e:  # noqa: BLE001
            seq = None
            print("erro", p.piece_id, e, flush=True)
        if seq is None:
            (out / f"{p.piece_id}__w{args.p}.skip").touch()
            continue
        x = torch.tensor([[AUTOREGRESS] + seq])
        with torch.no_grad():
            o = model(x, labels=x, output_hidden_states=True)
        hs = torch.stack(o.hidden_states)[:, 0]  # [13, T, 768]
        np.savez(out / f"{p.piece_id}__w{args.p}.npz",
                 last=hs[:, -1].numpy().astype(np.float16),
                 mean=hs[:, 1:].mean(1).numpy().astype(np.float16),
                 loss=np.float32(o.loss.item()), n_tokens=np.int32(x.shape[1]),
                 composer_key=p.composer_key, piece_id=p.piece_id, title=p.title)
        done += 1
    left = len(todo) - done
    print(f"feitas {done} em {(time.time() - t0) / 60:.1f} min; restam ~{left} nesta passada", flush=True)


if __name__ == "__main__":
    main()
