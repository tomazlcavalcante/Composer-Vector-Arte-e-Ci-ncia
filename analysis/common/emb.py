"""Leitura das representações extraídas (F0) e operações comuns das análises."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

pd.set_option("future.infer_string", False)  # strings como object (numpy puro nas comparações)

ROOT = Path(__file__).resolve().parents[2]
EMB_DIR = Path(os.environ.get("CV_EMBEDDINGS", "/home/claude/data/embeddings")) / "amt"


def load_meta() -> pd.DataFrame:
    return pd.read_csv(ROOT / "analysis" / "data" / "metadata_curated.csv")


def load(layer: int, pooling: str = "mean", windows=None, include_extra=False):
    """Retorna (X [n_janelas, 768] float32, df com piece_id, composer_key, window, loss)."""
    if windows is None:  # base de janelas fixada por ambiente (ex.: CV_WINDOWS=1,2)
        windows = tuple(int(w) for w in os.environ.get("CV_WINDOWS", "1,2,3").split(","))
    rows, vecs = [], []
    for f in sorted(EMB_DIR.glob("*.npz")):
        w = int(f.stem.rsplit("__w", 1)[1])
        if w not in windows:
            continue
        z = np.load(f)
        vecs.append(z[pooling][layer].astype(np.float32))
        rows.append(dict(piece_id=str(z["piece_id"]), composer_key=str(z["composer_key"]), window=w,
                         loss=float(z["loss"]), title=str(z["title"])))
    df = pd.DataFrame(rows)
    X = np.stack(vecs) if vecs else np.zeros((0, 768), np.float32)
    meta = load_meta()
    keep = df.composer_key.isin(meta.loc[meta.incluir == 1, "composer_key"])
    if not include_extra:
        X, df = X[keep.values], df[keep].reset_index(drop=True)
    return X, df


def piece_level(X, df):
    """Média das janelas de cada peça (fragmento -> peça)."""
    g = df.groupby("piece_id", sort=False)
    idx = [ix.values for _, ix in g.groups.items()]
    Xp = np.stack([X[i].mean(0) for i in idx])
    dp = df.groupby("piece_id", sort=False).agg(composer_key=("composer_key", "first"), title=("title", "first"),
                                                 loss=("loss", "mean"), n_windows=("window", "size")).reset_index()
    return Xp, dp


def center(X, mu=None):
    mu = X.mean(0) if mu is None else mu
    return X - mu, mu


def l2norm(X):
    return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)


def centroids(Xp, dp, min_pieces=1):
    """Centróide por compositor = média das peças (peça -> compositor)."""
    keys = [k for k, n in dp.composer_key.value_counts().items() if n >= min_pieces]
    keys = sorted(keys)
    C = np.stack([Xp[dp.composer_key.values == k].mean(0) for k in keys])
    return C, keys


def cosine_dist(A, B=None):
    A = l2norm(A)
    B = A if B is None else l2norm(B)
    return 1 - A @ B.T
