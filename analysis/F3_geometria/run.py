"""F3: geometria do mapa de compositores (Q1, hipóteses H1 e H2).

Lê a configuração escolhida na F2 (analysis/F2_representacao/metrics.json -> best).
Saídas: metrics.json, distancias.csv, afinidades.csv, figs/mapa_pca.png, figs/dist_vs_epoca.png
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

cfg = json.loads((HERE.parent / "F2_representacao" / "metrics.json").read_text())["best"]
LAYER, POOL = cfg["layer"], cfg["pooling"]
rng = np.random.default_rng(0)
(HERE / "figs").mkdir(exist_ok=True)
PERIOD_COLORS = {"Renascimento": "#8c564b", "Barroco": "#d62728", "Clássico": "#ff7f0e",
                 "Romântico": "#1f77b4", "Moderno": "#2ca02c"}

X, df = load(LAYER, POOL)
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp)
Z = l2norm(Xc)
C, keys = centroids(Z, dp)
D = cosine_dist(C)
n_by = dp.composer_key.value_counts()

# --- bootstrap por peças (IC das distâncias) ---
B = 200
boot = np.zeros((B,) + D.shape)
for b in range(B):
    Cb = []
    for k in keys:
        idx = np.where(dp.composer_key.values == k)[0]
        Cb.append(Z[rng.choice(idx, len(idx))].mean(0))
    boot[b] = cosine_dist(np.stack(Cb))
D_lo, D_hi = np.percentile(boot, [2.5, 97.5], axis=0)

# --- distância à média geral, contra nulo de rótulos permutados (mesmo n) ---
norm_c = np.linalg.norm(C, axis=1)  # média geral = 0 no espaço centrado
labels = dp.composer_key.values
null = np.zeros((200, len(keys)))
for b in range(200):
    perm = rng.permutation(labels)
    null[b] = [np.linalg.norm(Z[perm == k].mean(0)) for k in keys]
z_orig = (norm_c - null.mean(0)) / null.std(0)

meta = load_meta().set_index("composer_key").loc[keys]
dist_tab = pd.DataFrame(dict(composer=keys, n_pecas=[int(n_by[k]) for k in keys], birth=meta.birth.values,
                             periodo=meta.periodo.values, nacionalidade=meta.nationality.values,
                             dist_media_geral=norm_c.round(4), dist_media_nulo=null.mean(0).round(4),
                             z_originalidade=z_orig.round(2)))
dist_tab.sort_values("z_originalidade", ascending=False).to_csv(HERE / "distancias_media_geral.csv", index=False)

# --- Mantel: distância x |Δ nascimento| ; nacionalidade ---
iu = np.triu_indices(len(keys), 1)
birth = meta.birth.values.astype(float)
dyear = np.abs(birth[:, None] - birth[None, :])
same_nat = (meta.nationality.values[:, None] == meta.nationality.values[None, :]).astype(float)


def mantel(A, Bm, n_perm=10000):
    r0 = spearmanr(A[iu], Bm[iu]).statistic
    cnt = 0
    for _ in range(n_perm):
        p = rng.permutation(len(keys))
        if spearmanr(A[iu], Bm[p][:, p][iu]).statistic >= r0:
            cnt += 1
    return float(r0), (cnt + 1) / (n_perm + 1)


r_year, p_year = mantel(D, dyear, 5000)
r_nat, p_nat = mantel(-D, same_nat, 5000)  # mesma nacionalidade -> mais perto
# parcial: resíduo de D sobre Δano, depois nacionalidade
coef = np.polyfit(dyear[iu], D[iu], 1)
R = D.copy()
R[iu] = D[iu] - np.polyval(coef, dyear[iu])
R = np.triu(R, 1) + np.triu(R, 1).T
r_nat_partial, p_nat_partial = mantel(-R, same_nat, 5000)

# --- afinidades inesperadas: resíduos da regressão D ~ Δano ---
aff = pd.DataFrame(dict(a=[keys[i] for i in iu[0]], b=[keys[j] for j in iu[1]], dist=D[iu].round(4),
                        delta_ano=dyear[iu], residuo=R[iu].round(4),
                        ic_lo=D_lo[iu].round(4), ic_hi=D_hi[iu].round(4)))
aff.sort_values("residuo").to_csv(HERE / "afinidades.csv", index=False)

# --- vizinho mais próximo de cada compositor ---
Dn = D + np.eye(len(keys)) * 9
nn = pd.DataFrame(dict(composer=keys, vizinho=[keys[j] for j in Dn.argmin(1)], dist=Dn.min(1).round(4)))
nn.to_csv(HERE / "vizinhos.csv", index=False)

# --- PCA dos centróides + distorção ---
U, S, Vt = np.linalg.svd(C - C.mean(0), full_matrices=False)
P2 = (C - C.mean(0)) @ Vt[:2].T
expl = (S ** 2 / np.sum(S ** 2))[:2]
D2 = np.linalg.norm(P2[:, None] - P2[None], axis=-1)
distortion = spearmanr(D[iu], D2[iu]).statistic

fig, ax = plt.subplots(figsize=(11, 8.5))
for i, k in enumerate(keys):
    per = meta.periodo.values[i]
    ax.scatter(*P2[i], s=20 + 2 * n_by[k], color=PERIOD_COLORS.get(per, "gray"), alpha=0.8, edgecolor="white")
    ax.annotate(k.split(",")[0], P2[i], fontsize=8, xytext=(3, 3), textcoords="offset points")
for per, c in PERIOD_COLORS.items():
    ax.scatter([], [], color=c, label=per)
# Tico-Tico (ilustração)
Xe, de = load(LAYER, POOL, include_extra=True)
tt = de.composer_key.str.startswith("Abreu").values
if tt.any():
    zt = l2norm(Xe[tt].mean(0, keepdims=True) - mu)
    pt = (zt - C.mean(0)) @ Vt[:2].T
    ax.scatter(*pt[0], marker="*", s=220, color="black", label="Tico-Tico no Fubá (Abreu)")
    dtt = cosine_dist(zt, C)[0]
    tico = [dict(composer=keys[j], dist=round(float(dtt[j]), 4)) for j in np.argsort(dtt)[:5]]
else:
    tico = []
ax.legend(loc="best", fontsize=9)
ax.set_xlabel(f"PC1 ({expl[0]:.0%} da variância dos centróides)")
ax.set_ylabel(f"PC2 ({expl[1]:.0%})")
ax.set_title(f"Mapa dos compositores (AMT, camada {LAYER}, pooling {POOL})\n"
             f"Correlação de Spearman entre distâncias originais e projetadas: {distortion:.2f}", fontsize=11)
fig.tight_layout()
fig.savefig(HERE / "figs" / "mapa_pca.png", dpi=150)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(dyear[iu], D[iu], s=6, alpha=0.4)
ax.set_xlabel("|Δ ano de nascimento|")
ax.set_ylabel("distância cosseno entre centróides")
ax.set_title(f"H1: Mantel ρ = {r_year:.2f} (p = {p_year:.4f})")
fig.tight_layout()
fig.savefig(HERE / "figs" / "dist_vs_epoca.png", dpi=150)

out = dict(layer=LAYER, pooling=POOL, n_composers=len(keys), n_pieces=int(len(dp)),
           H1_mantel_rho=round(r_year, 4), H1_p=p_year,
           H2_nat_rho=round(r_nat, 4), H2_nat_p=p_nat, H2_nat_parcial_rho=round(r_nat_partial, 4),
           H2_nat_parcial_p=p_nat_partial, pca_explicada=expl.round(4).tolist(),
           pca_distorcao_spearman=round(float(distortion), 4), tico_tico_vizinhos=tico,
           dist_media_entre_centroides=round(float(D[iu].mean()), 4))
(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
