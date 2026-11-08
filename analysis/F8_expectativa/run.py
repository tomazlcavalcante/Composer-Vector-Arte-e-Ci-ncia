"""F8: surpresa média do modelo (perda por token) por compositor, época e período (ponte com Meyer).

Usa só a perda já salva em cada janela (campo `loss`, nats/token) e as janelas 1 e 2.
Saídas: metrics.json, surpresa_por_compositor.csv, figs/surpresa_por_compositor.png
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import spearmanr, kruskal  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, EMB_DIR  # noqa: E402

rng = np.random.default_rng(0)
B = 1000
PERIOD_COLORS = {"Renascimento": "#8c564b", "Barroco": "#d62728", "Clássico": "#ff7f0e",
                 "Romântico": "#1f77b4", "Moderno": "#2ca02c"}

X, df = load(6, "mean", windows=(1, 2))  # a camada não importa para a perda
_, dp = piece_level(X, df)               # dp.loss = média das janelas da peça
meta = load_meta().set_index("composer_key")
dp["birth"] = meta.loc[dp.composer_key, "birth"].values
dp["periodo"] = meta.loc[dp.composer_key, "periodo"].values

# --- 1. por compositor: média de peças + IC95% bootstrap de peças ---
rows = []
for k, g in dp.groupby("composer_key"):
    v = g.loss.values
    bm = np.array([rng.choice(v, len(v)).mean() for _ in range(B)])
    lo, hi = np.percentile(bm, [2.5, 97.5])
    rows.append(dict(composer_key=k, n_pecas=len(v), birth=int(meta.loc[k, "birth"]), periodo=meta.loc[k, "periodo"],
                     surpresa_media=v.mean(), ic95_lo=lo, ic95_hi=hi, dp_intra=v.std(ddof=1) if len(v) > 1 else np.nan,
                     mediana=np.median(v)))
tab = pd.DataFrame(rows).sort_values(["birth", "composer_key"]).reset_index(drop=True)
tab.round(4).to_csv(HERE / "surpresa_por_compositor.csv", index=False)

# --- 2. época ---
rho, p_rho = spearmanr(tab.birth, tab.surpresa_media)
rb = []
for _ in range(B):
    i = rng.integers(0, len(tab), len(tab))
    rb.append(spearmanr(tab.birth.values[i], tab.surpresa_media.values[i]).statistic)
rho_ci = np.nanpercentile(rb, [2.5, 97.5])
# nível de peça
rho_p, p_rho_p = spearmanr(dp.birth, dp.loss)
groups = {per: g.loss.values for per, g in dp.groupby("periodo")}
kw = kruskal(*groups.values())
eps2 = (kw.statistic - len(groups) + 1) / (len(dp) - len(groups))  # epsilon^2
per_tab = {per: dict(n_pecas=len(v), media=float(v.mean()), mediana=float(np.median(v)),
                     n_compositores=int(tab[tab.periodo == per].shape[0])) for per, v in groups.items()}
# nulo do KW: permutar períodos entre compositores (preserva a estrutura por compositor)
comp_per = tab.set_index("composer_key").periodo
kw_null = []
for _ in range(500):
    perm = dict(zip(comp_per.index, rng.permutation(comp_per.values)))
    pp = dp.composer_key.map(perm)
    kw_null.append(kruskal(*[dp.loss[pp == q].values for q in groups]).statistic)
p_kw_comp = (np.sum(np.array(kw_null) >= kw.statistic) + 1) / (len(kw_null) + 1)

# --- 3. controles / limitações ---
ntok = []
for f in sorted(EMB_DIR.glob("*.npz")):
    if int(f.stem.rsplit("__w", 1)[1]) in (1, 2):
        ntok.append(int(np.load(f)["n_tokens"]))
ntok = np.array(ntok)
# variância dentro do compositor vs. total (eta^2) com nulo de permutação
tot = dp.loss.var(ddof=0) * len(dp)
within = sum(((g.loss - g.loss.mean()) ** 2).sum() for _, g in dp.groupby("composer_key"))
eta2 = 1 - within / tot
nul = []
lab = dp.composer_key.values
for _ in range(500):
    pl = rng.permutation(lab)
    w = sum(((dp.loss.values[pl == k] - dp.loss.values[pl == k].mean()) ** 2).sum() for k in np.unique(pl))
    nul.append(1 - w / tot)
# confiabilidade janela 1 x janela 2 dentro da peça
wide = df.pivot_table(index="piece_id", columns="window", values="loss").dropna()
r_w = spearmanr(wide[1], wide[2]).statistic
# a surpresa por compositor se sustenta contando só uma janela? (consistência)
pm = df.groupby(["composer_key", "window"]).loss.mean().unstack()
r_c = spearmanr(pm[1], pm[2]).statistic
cv_intra = float((tab.dp_intra / tab.surpresa_media).median())
dp_ratio = float(tab.dp_intra.median() / tab.surpresa_media.std())

metrics = dict(
    config=dict(janelas=[1, 2], bootstrap=B, seed=0, n_janelas=int(len(df)), n_pecas=int(len(dp)),
                n_compositores=int(len(tab)), unidade_perda="nats/token (média da janela)"),
    geral=dict(media_pecas=float(dp.loss.mean()), dp_pecas=float(dp.loss.std()),
               min_compositor=tab.loc[tab.surpresa_media.idxmin(), ["composer_key", "surpresa_media"]].tolist(),
               max_compositor=tab.loc[tab.surpresa_media.idxmax(), ["composer_key", "surpresa_media"]].tolist(),
               dp_entre_compositores=float(tab.surpresa_media.std())),
    epoca=dict(spearman_compositor=dict(rho=float(rho), p=float(p_rho), ic95_bootstrap=rho_ci.tolist(), n=len(tab)),
               spearman_peca=dict(rho=float(rho_p), p=float(p_rho_p), n=len(dp)),
               kruskal_peca=dict(H=float(kw.statistic), p=float(kw.pvalue), epsilon2=float(eps2),
                                 p_nulo_permutando_periodo_entre_compositores=float(p_kw_comp)),
               por_periodo=per_tab),
    controles=dict(n_tokens=dict(min=int(ntok.min()), max=int(ntok.max()), mediana=float(np.median(ntok))),
                   eta2_compositor=float(eta2), eta2_nulo_media=float(np.mean(nul)), eta2_nulo_p95=float(np.percentile(nul, 95)),
                   spearman_janela1_janela2_dentro_da_peca=float(r_w),
                   spearman_compositor_j1_j2=float(r_c),
                   cv_intra_mediano=cv_intra, razao_dp_intra_sobre_dp_entre=dp_ratio),
)
(HERE / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))

# --- 4. figura ---
fig, ax = plt.subplots(figsize=(8, 11))
y = np.arange(len(tab))
for i, r in tab.iterrows():
    c = PERIOD_COLORS.get(r.periodo, "gray")
    ax.plot([r.ic95_lo, r.ic95_hi], [i, i], color=c, lw=1.6, alpha=0.8)
    ax.scatter(r.surpresa_media, i, color=c, s=28 + r.n_pecas * 0.5, edgecolor="white", zorder=3)
ax.axvline(dp.loss.mean(), color="gray", ls="--", lw=1)
ax.set_yticks(y)
ax.set_yticklabels([f"{r.composer_key.split(',')[0]}{'' if tab.composer_key.str.split(',').str[0].eq(r.composer_key.split(',')[0]).sum() == 1 else ' ' + r.composer_key.split(', ')[1][0] + '.'} ({r.birth}, n={r.n_pecas})" for _, r in tab.iterrows()], fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("Surpresa média do modelo (nats/token), IC95% bootstrap de peças")
ax.set_title("Surpresa do AMT por compositor, em ordem de nascimento\n(tracejado: média das peças)", fontsize=10)
for per, c in PERIOD_COLORS.items():
    ax.scatter([], [], color=c, label=per)
ax.legend(loc="upper right", fontsize=8, title="Período")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(HERE / "figs" / "surpresa_por_compositor.png", dpi=150)
print(json.dumps(metrics, indent=1, ensure_ascii=False))
print(tab.sort_values("surpresa_media")[["composer_key", "n_pecas", "birth", "periodo", "surpresa_media", "ic95_lo", "ic95_hi"]].round(3).to_string())
