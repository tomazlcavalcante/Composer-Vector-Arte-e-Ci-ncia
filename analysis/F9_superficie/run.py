"""F9: o modelo sabe mais que estatística de superfície? (PLANO_V2, bloco A; hipóteses H8–H11)

A2: mapa só com descritores simbólicos (padronizados) -> Mantel com época; RSA com o mapa do modelo.
A3: regredir os descritores para fora das representações do modelo (nível de peça) -> refazer H1, R², sonda.
A4: surpresa x época controlando descritores (correlação parcial, nível de compositor e de peça).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

rng = np.random.default_rng(0)
path = Path("/home/claude/data/descritores_janelas.parquet")
desc = pd.read_parquet(path) if path.exists() else pd.read_csv(path.with_suffix(".csv"))
desc = desc[desc.window.isin([1, 2])]
num = [c for c in desc.columns if c not in ("piece_id", "window", "composer_key", "title")]
dpiece = desc.groupby("piece_id")[num].mean()

X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
dp = dp[dp.piece_id.isin(dpiece.index)]
Xp = Xp[dp.index.values]
dp = dp.reset_index(drop=True)
D = dpiece.loc[dp.piece_id, num].values.astype(float)
D = np.nan_to_num((D - np.nanmean(D, 0)) / (np.nanstd(D, 0) + 1e-9))
y = dp.composer_key.values
meta = load_meta().set_index("composer_key")
out = dict(n_pecas=int(len(dp)), descritores=num)


def mantel_birth(Cmat, keys, n_perm=5000):
    Dm = cosine_dist(Cmat) if Cmat.shape[1] > 0 else None
    b = meta.loc[keys, "birth"].values.astype(float)
    dy = np.abs(b[:, None] - b[None])
    iu = np.triu_indices(len(keys), 1)
    r0 = spearmanr(Dm[iu], dy[iu]).statistic
    cnt = sum(spearmanr(Dm[iu], dy[np.ix_(p, p)][iu]).statistic >= r0
              for p in (rng.permutation(len(keys)) for _ in range(n_perm)))
    return float(r0), (cnt + 1) / (n_perm + 1), Dm


def r2(Z, y):
    tot = np.sum((Z - Z.mean(0)) ** 2)
    return float(sum((y == k).sum() * np.sum((Z[y == k].mean(0) - Z.mean(0)) ** 2) for k in set(y)) / tot)


def probe(Z, y):
    pred = cross_val_predict(LogisticRegression(max_iter=3000), Z, y, cv=StratifiedKFold(5, shuffle=True, random_state=0))
    return float(balanced_accuracy_score(y, pred))


# modelo (base)
Zm = l2norm(center(Xp)[0])
Cm, keys = centroids(Zm, dp)
r_m, p_m, Dmod = mantel_birth(Cm, keys)
out["modelo"] = dict(H1_mantel=round(r_m, 3), p=p_m, R2=round(r2(Zm, y), 3), sonda=round(probe(Zm, y), 3))

# A2: descritores sozinhos (distância euclidiana padronizada também reportada via cosseno nos centróides centrados)
Cd = np.stack([D[y == k].mean(0) for k in keys])
Cd = Cd - Cd.mean(0)
r_d, p_d, Ddesc = mantel_birth(Cd, keys)
iu = np.triu_indices(len(keys), 1)
rsa = spearmanr(Dmod[iu], Ddesc[iu]).statistic
out["A2_descritores"] = dict(H8_mantel=round(r_d, 3), p=p_d, R2=round(r2(D, y), 3), sonda=round(probe(D, y), 3),
                             H9_rsa_modelo_vs_descritores=round(float(rsa), 3))

# A3: resíduos do modelo após regredir os descritores
res = Xp - LinearRegression().fit(D, Xp).predict(D)
Zr = l2norm(res - res.mean(0))
Cr, _ = centroids(Zr, dp)
r_r, p_r, _ = mantel_birth(Cr, keys)
var_expl = 1 - np.sum((res - res.mean(0)) ** 2) / np.sum((Xp - Xp.mean(0)) ** 2)
out["A3_residuos"] = dict(H10_mantel=round(r_r, 3), p=p_r, R2=round(r2(Zr, y), 3), sonda=round(probe(Zr, y), 3),
                          frac_variancia_do_modelo_explicada_pelos_descritores=round(float(var_expl), 3))

# A4: surpresa x época controlando descritores
loss = dp.loss.values
birth_p = meta.loc[y, "birth"].values.astype(float)
lres = loss - LinearRegression().fit(D, loss).predict(D)
comp = pd.DataFrame(dict(k=y, loss=loss, lres=lres, b=birth_p)).groupby("k").mean()
out["A4_surpresa"] = dict(
    rho_compositor_bruto=round(float(spearmanr(comp.loss, comp.b).statistic), 3),
    rho_compositor_controlado=round(float(spearmanr(comp.lres, comp.b).statistic), 3),
    rho_peca_bruto=round(float(spearmanr(loss, birth_p).statistic), 3),
    rho_peca_controlado=round(float(spearmanr(lres, birth_p).statistic), 3),
    R2_surpresa_explicada_pelos_descritores=round(float(LinearRegression().fit(D, loss).score(D, loss)), 3))
# p por permutação (nível de compositor) para o controlado
null = [spearmanr(comp.lres.values, rng.permutation(comp.b.values)).statistic for _ in range(5000)]
out["A4_surpresa"]["p_compositor_controlado"] = float((np.sum(np.abs(null) >= abs(out["A4_surpresa"]["rho_compositor_controlado"])) + 1) / 5001)

(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in out.items() if k != "descritores"}, indent=1, ensure_ascii=False))
