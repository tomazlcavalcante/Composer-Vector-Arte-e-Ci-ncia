"""Figura do slide 5: peças nos eixos da PCA dos centróides (mesmos do explorador), nuvens de 4 compositores."""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids

X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp); Z = l2norm(Xc)
C, keys = centroids(Z, dp)
Cm = C.mean(0)
U, S, Vt = np.linalg.svd(C - Cm, full_matrices=False)
meta = load_meta().set_index("composer_key")
birth = meta.loc[keys, "birth"].values.astype(float)
if np.corrcoef((C - Cm) @ Vt[0], birth)[0, 1] < 0: Vt[0] *= -1
Pp = (Z - Cm) @ Vt[:2].T
P = (C - Cm) @ Vt[:2].T
expl = (S**2 / (S**2).sum())[:2]
m = json.load(open(HERE / "metrics.json"))
r2, nulo, sob = m["H3_R2_compositor"], m["H3_R2_nulo_media"], m["sobreposicao_frac_pecas_mais_perto_de_outro"]
print(len(dp), expl, r2, nulo, sob)

sel = [("Bach, Johann Sebastian", "Bach", "#1b6ca8"), ("Mozart, Wolfgang Amadeus", "Mozart", "#d98e04"),
       ("Chopin, Frédéric", "Chopin", "#b5304a"), ("Joplin, Scott", "Joplin", "#2a8c4a")]
fig, ax = plt.subplots(figsize=(12, 7.6), dpi=170)
ax.scatter(Pp[:, 0], Pp[:, 1], s=7, c="#d4d4d4", lw=0, label=f"todas as {len(dp):,} peças".replace(",", "."), zorder=1)
offs = {"Bach": (14, -22), "Mozart": (14, 14), "Chopin": (14, 12), "Joplin": (-10, 26)}
for k, nome, cor in sel:
    mk = dp.composer_key.values == k
    pts = Pp[mk]; mean = pts.mean(0); cov = np.cov(pts.T)
    w, v = np.linalg.eigh(cov); o = w.argsort()[::-1]; w, v = w[o], v[:, o]
    ang = np.degrees(np.arctan2(v[1, 0], v[0, 0]))
    ax.add_patch(Ellipse(mean, 2*np.sqrt(w[0]), 2*np.sqrt(w[1]), angle=ang, fc=cor, alpha=0.13, ec=cor, lw=2, zorder=2))
    ax.scatter(pts[:, 0], pts[:, 1], s=16, c=cor, alpha=0.65, lw=0, zorder=3)
    c = P[keys.index(k)]
    ax.scatter(*c, s=260, c=cor, ec="white", lw=2, zorder=5)
    ax.annotate(f"{nome} (n={mk.sum()})", c, xytext=offs[nome], textcoords="offset points", fontsize=13, fontweight="bold",
                color=cor, zorder=6, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1.5))
ax.set_xlabel(f"PC1 ({expl[0]:.0%} da variação entre centróides; cresce com o nascimento)", fontsize=11)
ax.set_ylabel(f"PC2 ({expl[1]:.0%})", fontsize=11)
ax.tick_params(labelsize=9)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.suptitle("As obras de cada compositor formam nuvens largas que se cruzam", x=0.06, ha="left", fontsize=20, fontweight="bold", y=0.975)
fig.text(0.06, 0.905, f"o compositor explica {r2:.0%} da variação entre peças (nulo: {nulo:.0%}); {sob:.0%} das peças ficam mais perto do centro de outro compositor",
         fontsize=12.5, color="#333")
fig.text(0.06, 0.012, "Cada ponto é uma peça; elipse = 1 desvio-padrão das peças do compositor; ponto grande = centróide. Projeção 2D (PCA dos 52 centróides, camada 6): "
         "distorce as distâncias,\nentão sobreposições aqui não medem as do espaço original de 768 dimensões.", fontsize=9.5, color="#555", va="bottom")
ax.legend(loc="lower right", frameon=False, fontsize=10, markerscale=2)
fig.subplots_adjust(top=0.86, bottom=0.15, left=0.07, right=0.97)
(HERE / "figs").mkdir(exist_ok=True)
fig.savefig(HERE / "figs" / "nuvens_pecas.png")
