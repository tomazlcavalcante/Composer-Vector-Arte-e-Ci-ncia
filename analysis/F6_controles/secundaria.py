"""F6: as conclusões principais dependem da escolha fina da representação?

Recalcula H1 (Mantel distância x |Δ nascimento|), H2 parcial (nacionalidade controlando época),
H3 (R² do compositor) e o grupo estável k = 2 (ligação média) para várias configurações:
a principal (camada 6, média), a secundária da F2 (camada 5, média), a última camada (12, média)
e a configuração do artigo/repo original (último token) na camada 6.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

rng = np.random.default_rng(0)
meta_all = load_meta().set_index("composer_key")
out = {}
for layer, pool in [(6, "mean"), (5, "mean"), (12, "mean"), (6, "last")]:
    X, df = load(layer, pool, windows=(1, 2))
    Xp, dp = piece_level(X, df)
    Z = l2norm(center(Xp)[0])
    C, keys = centroids(Z, dp)
    D = cosine_dist(C)
    meta = meta_all.loc[keys]
    iu = np.triu_indices(len(keys), 1)
    birth = meta.birth.values.astype(float)
    dy = np.abs(birth[:, None] - birth[None])
    r0 = spearmanr(D[iu], dy[iu]).statistic
    null = []
    for _ in range(1000):
        p = rng.permutation(len(keys))
        null.append(spearmanr(D[iu], dy[p][:, p][iu]).statistic)
    nat = (meta.nationality.values[:, None] == meta.nationality.values[None]).astype(float)
    coef = np.polyfit(dy[iu], D[iu], 1)
    res = D[iu] - np.polyval(coef, dy[iu])
    r_nat = spearmanr(-res, nat[iu]).statistic
    y = dp.composer_key.values
    tot = np.sum((Z - Z.mean(0)) ** 2)
    r2 = sum((y == k).sum() * np.sum((Z[y == k].mean(0) - Z.mean(0)) ** 2) for k in set(y)) / tot
    Ds = D.copy()
    np.fill_diagonal(Ds, 0)
    cl = fcluster(linkage(squareform(np.clip((Ds + Ds.T) / 2, 0, None), checks=False), "average"), 2, "maxclust")
    small = min(set(cl), key=lambda g: (cl == g).sum())
    out[f"camada{layer}_{pool}"] = dict(
        H1_mantel=round(float(r0), 3), H1_p=round(float((np.sum(np.array(null) >= r0) + 1) / 1001), 4),
        H2_nat_parcial=round(float(r_nat), 3), H3_R2=round(float(r2), 3),
        grupo_menor_k2=[keys[i].split(",")[0] for i in np.where(cl == small)[0]])
    print(f"camada{layer}_{pool}", out[f"camada{layer}_{pool}"], flush=True)
(HERE / "metrics_secundaria.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
