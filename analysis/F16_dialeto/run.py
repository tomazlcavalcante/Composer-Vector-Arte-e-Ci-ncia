"""F16 / H18: dialeto nacional dentro de uma época (só românticos).

Centróides como em F3 (camada 6, mean, janelas 1 e 2, sem duplicatas, peças centradas e L2-normalizadas).
Mantel parcial: resíduo da distância cosseno numa regressão linear em |Δ nascimento|; Spearman do resíduo (negado)
com a indicadora de mesma nacionalidade; p unicaudal (ρ > 0) por 5.000 permutações dos rótulos de nacionalidade.
Saídas: metrics.json, nacionalidades.csv
"""
import json, os, sys
from pathlib import Path
os.environ["CV_WINDOWS"] = "1,2"
import numpy as np, pandas as pd
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist

rng = np.random.default_rng(0)
X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp); Z = l2norm(Xc)         # centragem na base inteira, como em F3
meta_all = load_meta().set_index("composer_key")
rom = set(meta_all.index[(meta_all.periodo == "Romântico") & (meta_all.incluir == 1)])
sel = dp.composer_key.isin(rom).values
Zr, dr = Z[sel], dp[sel].reset_index(drop=True)
C, keys = centroids(Zr, dr)
n = len(keys)
D = cosine_dist(C)
meta = meta_all.loc[keys]
nat = meta.nationality.values
birth = meta.birth.values.astype(float)
iu = np.triu_indices(n, 1)
dyear = np.abs(birth[:, None] - birth[None, :])
coef = np.polyfit(dyear[iu], D[iu], 1)
res = D[iu] - np.polyval(coef, dyear[iu])
rres = rankdata(-res)                        # mesma nacionalidade -> mais perto -> resíduo negativo

def stat(labels):
    same = (labels[:, None] == labels[None, :])[iu].astype(float)
    if same.std() == 0: return np.nan
    return float(np.corrcoef(rres, rankdata(same))[0, 1])

r0 = stat(nat)
null = np.array([stat(rng.permutation(nat)) for _ in range(5000)])
p = float((np.sum(null >= r0) + 1) / (len(null) + 1))
# não parcial (referência)
rraw = rankdata(-D[iu])
same0 = (nat[:, None] == nat[None, :])[iu].astype(float)
r_raw = float(np.corrcoef(rraw, rankdata(same0))[0, 1])
r_year = float(np.corrcoef(rankdata(D[iu]), rankdata(dyear[iu]))[0, 1])

# nacionalidades com >= 3 românticos
rows = []
for g in sorted(set(nat)):
    m = nat == g
    if m.sum() < 3: continue
    inner = D[np.ix_(m, m)][np.triu_indices(m.sum(), 1)].mean()
    outer = D[np.ix_(m, ~m)].mean()
    rows.append(dict(nacionalidade=g, n_compositores=int(m.sum()), dist_interna=round(float(inner), 4),
                     dist_aos_outros=round(float(outer), 4), diferenca=round(float(outer - inner), 4),
                     compositores="; ".join(np.array(keys)[m])))
T = pd.DataFrame(rows).sort_values("n_compositores", ascending=False)
T.to_csv(HERE / "nacionalidades.csv", index=False)
out = dict(n_romanticos=n, n_pecas=int(len(dr)), n_pares=int(len(iu[0])), n_pares_mesma_nac=int(same0.sum()),
           contagem_nacionalidades=pd.Series(nat).value_counts().to_dict(),
           rho_dist_vs_dnasc=round(r_year, 4), coef_linear=[float(c) for c in coef],
           rho_nac_bruto=round(r_raw, 4), rho_parcial=round(r0, 4), p_unicaudal=p,
           nulo_media=round(float(null.mean()), 4), nulo_p95=round(float(np.percentile(null, 95)), 4), n_perm=5000)
(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False)); print(T.drop(columns="compositores").to_string())
