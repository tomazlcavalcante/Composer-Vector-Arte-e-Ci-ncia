"""A1: descritores simbólicos por janela (sem o modelo). Ver DESCRITORES.md.
Reconstrói cada janela com window() de F0 e calcula descritores a partir dos eventos.
Uso: nice -n 5 python3 analysis/F9_superficie/descritores_janelas.py
Retomável: parciais em /home/claude/data/descritores_parcial/.
"""
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, "/home/claude/ext/anticipation")
from analysis.common.data import list_pieces  # noqa: E402
from anticipation.convert import midi_to_events  # noqa: E402
from anticipation.vocab import DUR_OFFSET, NOTE_OFFSET, TIME_OFFSET  # noqa: E402

EMB = Path("/home/claude/data/embeddings/amt")
MIDIS = "/home/claude/data/giant/surname_checked_midis"
OUT = Path("/home/claude/data/descritores_janelas")
PART = Path("/home/claude/data/descritores_parcial")
FRACTIONS = {1: 0.5, 2: 1 / 6}
CHUNK = 500


def window(events, frac):  # cópia fiel de F0_infra/extract_amt.window (sem importar torch/transformers)
    from anticipation import ops
    n_ev = len(events) // 3
    if n_ev < 60:
        return None
    N_EVENTS = 341
    start_ev = max(0, min(n_ev - N_EVENTS, int(frac * n_ev) - N_EVENTS // 2))
    seq = events[3 * start_ev: 3 * (start_ev + N_EVENTS)]
    seq = ops.translate(seq, -ops.min_time(seq, seconds=False), seconds=False)
    keep = [i for i in range(0, len(seq), 3) if seq[i] - 0 < 100 * 100]
    seq = [t for i in keep for t in seq[i:i + 3]]
    return seq if len(seq) >= 180 else None


def descritores(seq):
    a = np.asarray(seq).reshape(-1, 3)
    on = (a[:, 0] - TIME_OFFSET).astype(float) * 0.01   # s
    du = (a[:, 1] - DUR_OFFSET).astype(float) * 0.01    # s
    pit = ((a[:, 2] - NOTE_OFFSET) % 128).astype(float)
    n = len(a)
    ut, inv, cnt = np.unique(on, return_inverse=True, return_counts=True)
    span = max(float((on + du).max() - on.min()), 1e-6)
    d = {"n_notas": n, "span_s": span, "notas_por_s": n / span,
         "altura_media": pit.mean(), "altura_dp": pit.std(),
         "extensao": np.percentile(pit, 95) - np.percentile(pit, 5),
         "duracao_media_s": du.mean()}
    grid = np.arange(0, on.max() + 1e-9, 0.05)
    # notas soando em cada instante: onset <= t < onset+dur
    d["polifonia_media"] = float(((on[None, :] <= grid[:, None]) & (grid[:, None] < (on + du)[None, :])).sum(1).mean())
    ioi = np.diff(ut)
    ioi = ioi[ioi > 0]
    d["ioi_mediano_s"] = float(np.median(ioi)) if len(ioi) else np.nan
    d["frac_acordes"] = float((cnt[inv] > 1).mean())  # fração de notas cujo ataque é compartilhado
    top = np.zeros(len(ut))
    np.maximum.at(top, inv, pit)
    d["intervalo_melodico_medio"] = float(np.abs(np.diff(top)).mean()) if len(top) > 1 else np.nan
    h = np.bincount((pit % 12).astype(int), weights=du, minlength=12)
    h = h / h.sum() if h.sum() > 0 else np.full(12, 1 / 12)
    for i in range(12):
        d[f"pc{i}"] = h[i]
    p = h[h > 0]
    d["entropia_pc"] = float(-(p * np.log2(p)).sum())
    return d


def work(item):
    pid, comp, k, path = item
    try:
        seq = window(midi_to_events(path), FRACTIONS[k])
        if seq is None:
            return None
        r = {"piece_id": pid, "composer_key": comp, "window": k}
        r.update(descritores(seq))
        return r
    except Exception as e:  # noqa: BLE001
        print("erro", pid, k, e, flush=True)
        return None


def main():
    t0 = time.time()
    PART.mkdir(exist_ok=True)
    pieces = {p.piece_id: p for p in list_pieces(MIDIS)}
    items = []
    for k in (1, 2):
        for f in sorted(EMB.glob(f"*__w{k}.npz")):
            pid = f.name[:-len(f"__w{k}.npz")]
            items.append((pid, pieces[pid].composer_key, k, str(pieces[pid].path)))
    print(len(items), "janelas", flush=True)
    chunks = [items[i:i + CHUNK] for i in range(0, len(items), CHUNK)]
    with Pool(2) as pool:
        for ci, ch in enumerate(chunks):
            f = PART / f"parte_{ci:03d}.pkl"
            if f.exists():
                continue
            rows = [r for r in pool.map(work, ch, chunksize=10) if r]
            pd.DataFrame(rows).to_pickle(f)
            print(f"parte {ci + 1}/{len(chunks)} ({time.time() - t0:.0f}s)", flush=True)
    df = pd.concat([pd.read_pickle(PART / f"parte_{i:03d}.pkl") for i in range(len(chunks))], ignore_index=True)
    try:
        df.to_parquet(OUT.with_suffix(".parquet"), index=False)
        print("parquet")
    except Exception:  # noqa: BLE001
        df.to_csv(OUT.with_suffix(".csv"), index=False)
        print("csv (sem parquet)")
    print(len(df), "linhas;", f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
