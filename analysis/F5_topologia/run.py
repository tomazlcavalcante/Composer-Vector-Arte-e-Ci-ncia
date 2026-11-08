"""F5: forma do espaço (Q3, hipótese H5).

Homologia persistente de grau 0 sobre os centróides (equivalente ao dendrograma de ligação simples),
comparada a um nulo sem grupos: gaussiana com a mesma média e covariância dos centróides. Barras de H0 muito
mais longas que no nulo indicam grupos separados; barras parecidas com o nulo indicam um contínuo.
Também: dendrograma (ligação média, só ilustrativo) colorido por período e estabilidade em bootstrap
dos grupos (índice de Rand ajustado ao cortar em k = 2..5).
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster  # noqa: E402
from scipy.spatial.distance import squareform  # noqa: E402
from sklearn.metrics import adjusted_rand_score  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

cfg = json.loads((HERE.parent / "F2_representacao" / "metrics.json").read_text())["best"]
LAYER, POOL = cfg["layer"], cfg["pooling"]
rng = np.random.default_rng(0)
(HERE / "figs").mkdir(exist_ok=True)

X, df = load(LAYER, POOL)
Xp, dp = piece_level(X, df)
Z = l2norm(center(Xp)[0])
C, keys = centroids(Z, dp)
D = cosine_dist(C)
np.fill_diagonal(D, 0)
D = np.clip((D + D.T) / 2, 0, None)


def h0_bars(D):
    """Comprimentos das barras finitas de H0 = alturas de fusão da ligação simples."""
    return np.sort(linkage(squareform(D, checks=False), "single")[:, 2])


bars = h0_bars(D)
null = []
y = dp.composer_key.values
# nulo sem estrutura de grupos: gaussiana com a mesma média e covariância dos centróides
mC, covC = C.mean(0), np.cov(C, rowvar=False)
for _ in range(200):
    Cn = rng.multivariate_normal(mC, covC, size=len(keys), method="eigh")
    Dn = cosine_dist(Cn)
    np.fill_diagonal(Dn, 0)
    null.append(h0_bars(np.clip((Dn + Dn.T) / 2, 0, None)))
null = np.array(null)
# razão: maior lacuna (última fusão) vs. distribuição das fusões
gap_ratio = float(bars[-1] / np.median(bars))
gap_ratio_null = null[:, -1] / np.median(null, axis=1)

# estabilidade de grupos (ligação média) em bootstrap por peças
L = linkage(squareform(D, checks=False), "average")
ari = {}
for k in range(2, 6):
    base = fcluster(L, k, "maxclust")
    vals = []
    for _ in range(100):
        Cb = np.stack([Z[rng.choice(np.where(y == kk)[0], (y == kk).sum())].mean(0) for kk in keys])
        Db = cosine_dist(Cb)
        np.fill_diagonal(Db, 0)
        Lb = linkage(squareform(np.clip((Db + Db.T) / 2, 0, None), checks=False), "average")
        vals.append(adjusted_rand_score(base, fcluster(Lb, k, "maxclust")))
    ari[k] = round(float(np.mean(vals)), 3)
meta = load_meta().set_index("composer_key").loc[keys]
groups = {k: {int(g): [keys[i].split(",")[0] for i in np.where(fcluster(L, k, "maxclust") == g)[0]]
              for g in set(fcluster(L, k, "maxclust"))} for k in range(2, 5)}

cols = {"Renascimento": "#8c564b", "Barroco": "#d62728", "Clássico": "#ff7f0e", "Romântico": "#1f77b4", "Moderno": "#2ca02c"}
fig, ax = plt.subplots(figsize=(8, 11))
dn = dendrogram(L, labels=[k.split(",")[0] for k in keys], orientation="left", ax=ax, color_threshold=0,
                above_threshold_color="#888")
for lbl in ax.get_ymajorticklabels():
    i = [k.split(",")[0] for k in keys].index(lbl.get_text())
    lbl.set_color(cols.get(meta.periodo.values[i], "gray"))
ax.set_title(f"Dendrograma dos centróides (ligação média, cosseno)\ncor do nome = período; estabilidade ARI k=2..5: {ari}", fontsize=10)
fig.tight_layout()
fig.savefig(HERE / "figs" / "dendrograma.png", dpi=150)

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(bars, "o-", label="dados", ms=3)
ax.fill_between(range(len(bars)), np.percentile(null, 5, 0), np.percentile(null, 95, 0), alpha=0.3, label="nulo 90%")
ax.set_xlabel("ordem da fusão (H0)")
ax.set_ylabel("distância de fusão (ligação simples)")
ax.set_title("Barras de H0: grupos separados ou contínuo?")
ax.legend()
fig.tight_layout()
fig.savefig(HERE / "figs" / "h0_barras.png", dpi=150)

out = dict(layer=LAYER, pooling=POOL, h0_maior_barra=round(float(bars[-1]), 4), h0_mediana=round(float(np.median(bars)), 4),
           gap_ratio=round(gap_ratio, 3), gap_ratio_nulo_p95=round(float(np.percentile(gap_ratio_null, 95)), 3),
           ari_bootstrap=ari, grupos_ligacao_media=groups)
(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
