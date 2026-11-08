"""F15 / H17: o que o eixo do tempo do mapa "ouve"? Spearman de PC1 e PC2 com descritores simbólicos simples.

Base: camada 6, mean, janelas 1 e 2 (CV_WINDOWS=1,2), sem duplicatas. PCA dos centróides como em D1_explorador/export.py
(PC1 orientado pelo nascimento; PC2 com o sinal arbitrário do SVD). Peças projetadas nos mesmos eixos.
Saídas: metrics.json, correlacoes.csv, figs/eixos_descritores.png
"""
import json, os, sys
from pathlib import Path
os.environ["CV_WINDOWS"] = "1,2"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from scipy.stats import rankdata, spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids

rng = np.random.default_rng(0)
N_PERM = 10000
X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp); Z = l2norm(Xc)
C, keys = centroids(Z, dp)
Cm = C.mean(0)
U, S, Vt = np.linalg.svd(C - Cm, full_matrices=False)
meta = load_meta().set_index("composer_key")
birth = meta.loc[keys, "birth"].values.astype(float)
if np.corrcoef((C - Cm) @ Vt[0], birth)[0, 1] < 0: Vt[0] *= -1
Pp = (Z - Cm) @ Vt[:2].T          # peças
Pc = (C - Cm) @ Vt[:2].T          # compositores (centróides)
expl = (S**2 / (S**2).sum())[:2]

DESC = ["entropia_pc", "polifonia_media", "extensao", "notas_por_s", "ioi_mediano_s", "frac_acordes",
        "duracao_media_s", "intervalo_melodico_medio", "altura_media", "altura_dp"]
d = pd.read_csv("/home/claude/data/descritores_janelas.csv")
d = d[d.window.isin([1, 2])].groupby("piece_id")[DESC].mean()
dd = dp[["piece_id", "composer_key"]].join(d, on="piece_id")
miss = int(dd[DESC].isna().any(axis=1).sum())
ok = ~dd[DESC].isna().any(axis=1).values
dd, Pp_ok = dd[ok].reset_index(drop=True), Pp[ok]
comp_desc = dd.groupby("composer_key")[DESC].mean().loc[keys]


def perm_spearman(x, y):
    """rho de Spearman e p bicaudal / unicaudais por permutação (compositores)."""
    rx, ry = rankdata(x), rankdata(y)
    r0 = np.corrcoef(rx, ry)[0, 1]
    n = len(rx)
    idx = np.argsort(rng.random((N_PERM, n)), axis=1)
    rp = np.array([np.corrcoef(rx, ry[i])[0, 1] for i in idx])
    p2 = (np.sum(np.abs(rp) >= abs(r0)) + 1) / (N_PERM + 1)
    pg = (np.sum(rp >= r0) + 1) / (N_PERM + 1)
    pl = (np.sum(rp <= r0) + 1) / (N_PERM + 1)
    return float(r0), float(p2), float(pg), float(pl)


rows = []
for ax_i, ax in enumerate(["PC1", "PC2"]):
    for c in DESC:
        rp_, pp_ = spearmanr(Pp_ok[:, ax_i], dd[c].values)
        rc, p2, pg, pl = perm_spearman(Pc[:, ax_i], comp_desc[c].values)
        rows.append(dict(eixo=ax, descritor=c, rho_peca=rp_, p_peca=pp_, rho_compositor=rc, p_perm_2caudas=p2,
                         p_perm_rho_maior=pg, p_perm_rho_menor=pl))
R = pd.DataFrame(rows)
R.round(4).to_csv(HERE / "correlacoes.csv", index=False)

# --- figura ---
lab = {"entropia_pc": "Entropia de classes de altura\n(cromatismo)", "polifonia_media": "Polifonia média",
       "extensao": "Extensão (p95 − p5)", "notas_por_s": "Notas por segundo", "ioi_mediano_s": "IOI mediano (s)",
       "frac_acordes": "Fração de acordes", "duracao_media_s": "Duração média das notas",
       "intervalo_melodico_medio": "Intervalo melódico médio", "altura_media": "Altura média", "altura_dp": "Dispersão da altura"}
fig, axs = plt.subplots(1, 2, figsize=(13, 6.2), sharey=True)
order = DESC[::-1]
for a, ax in zip(axs, ["PC1", "PC2"]):
    sub = R[R.eixo == ax].set_index("descritor").loc[order]
    y = np.arange(len(order)); h = 0.38
    a.barh(y + h/2, sub.rho_peca, h, color="#1f77b4", label=f"peças (n = {len(dd)})")
    a.barh(y - h/2, sub.rho_compositor, h, color="#ff7f0e", label=f"compositores (n = {len(keys)})")
    a.axvline(0, color="k", lw=0.8); a.set_xlim(-1, 1)
    a.set_yticks(y); a.set_yticklabels([lab[c] for c in order], fontsize=9)
    a.set_xlabel("ρ de Spearman"); a.grid(axis="x", alpha=0.3)
    a.set_title(f"{ax} ({expl[0 if ax == 'PC1' else 1]:.0%} da variância)" + (" — eixo cronológico" if ax == "PC1" else " — sinal arbitrário"), fontsize=10)
axs[0].legend(fontsize=8, loc="lower left")
fig.suptitle("O eixo do tempo do modelo acompanha sobretudo a polifonia e a duração das notas (ρ ≈ 0,85 entre compositores), e menos o cromatismo (ρ ≈ 0,60)", fontsize=12, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(HERE / "figs" / "eixos_descritores.png", dpi=150)
(HERE / "metrics.json").write_text(json.dumps(dict(n_pecas=int(len(dd)), n_pecas_sem_descritor=miss, n_compositores=len(keys),
    pca_explicada=expl.round(4).tolist(), n_perm=N_PERM), indent=1))
print(R.round(3).to_string()); print(len(dd), miss, len(keys), expl)
