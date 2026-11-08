"""Figura-síntese de F9/F10: A cronologia sobrevive aos controles. Nulo: 1.000 permutações dos rótulos
(nascimento) entre os centróides do modelo; p95 do Spearman (distância cosseno x |Δ nascimento|)."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

m9 = json.load(open(HERE / "metrics.json"))
m10 = json.load(open(HERE.parent / "F10_genero" / "metrics.json"))

X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Xp = l2norm(center(Xp)[0])
C, keys = centroids(Xp, dp)
meta = load_meta().set_index("composer_key")
b = meta.loc[keys, "birth"].values.astype(float)
Dm = cosine_dist(C)
iu = np.triu_indices(len(keys), 1)
dy = np.abs(b[:, None] - b[None])
rng = np.random.default_rng(0)
nulo = np.array([spearmanr(Dm[iu], dy[np.ix_(p, p)][iu]).statistic
                 for p in (rng.permutation(len(keys)) for _ in range(1000))])
p95 = float(np.percentile(nulo, 95))
print("obs", spearmanr(Dm[iu], dy[iu]).statistic, "p95", p95, "max", nulo.max())

rows = [("Modelo (base)", m9["modelo"]["H1_mantel"]),
        ("Modelo sem gênero (título)", m10["residuos_de_genero"]["mantel_rho"]),
        ("Modelo sem estatísticas de superfície", m9["A3_residuos"]["H10_mantel"]),
        ("Só estatísticas de superfície (sem o modelo)", m9["A2_descritores"]["H8_mantel"])]
fmt = lambda v: f"{v:.2f}".replace(".", ",") if v < 0.35 and False else f"{v:.3f}".replace(".", ",")
cols = ["#2f5d8a", "#5b8db8", "#5b8db8", "#b0b0b0"]
fig, ax = plt.subplots(figsize=(8.5, 3.9))
y = np.arange(len(rows))[::-1]
ax.barh(y, [r[1] for r in rows], color=cols, height=0.6)
for yi, (_, v) in zip(y, rows):
    ax.text(v + 0.008, yi, fmt(v), va="center", fontsize=10)
ax.axvline(p95, color="#c0392b", ls="--", lw=1.3)
ax.text(p95 + 0.006, y[0] + 0.5, f"p95 do nulo ≈ {fmt(p95)}", color="#c0392b", fontsize=9, va="bottom")
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=10)
ax.set_xlim(0, 0.62); ax.set_ylim(-0.6, y[0] + 0.95)
ax.set_xlabel("Mantel ρ (distância entre compositores × diferença de nascimento)")
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",")))
ax.set_title("A cronologia sobrevive aos controles", fontsize=12, loc="left", fontweight="bold")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.text(0.01, 0.01, "52 compositores, camada 6, 2 janelas por peça. Nulo: 1.000 permutações dos nascimentos entre os centróides do modelo.",
         fontsize=7.5, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(HERE / "figs" / "controles_cronologia.png", dpi=150)
