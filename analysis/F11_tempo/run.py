"""F11 (C1): à frente ou atrás do seu tempo? Resíduo de PC1 ~ nascimento, IC por bootstrap de peças.
Base sem controle de gênero: camada 6, média, janelas 1 e 2 (como F3)."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from adjustText import adjust_text  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids  # noqa: E402

rng = np.random.default_rng(0)
(HERE / "figs").mkdir(exist_ok=True)
COLORS = {"Renascimento": "#8c564b", "Barroco": "#d62728", "Clássico": "#ff7f0e", "Romântico": "#1f77b4", "Moderno": "#2ca02c"}

X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Z = l2norm(center(Xp)[0])
C, keys = centroids(Z, dp)
y = dp.composer_key.values
meta = load_meta().set_index("composer_key").loc[keys]
birth = meta.birth.values.astype(float)

mu = C.mean(0)
U, S, Vt = np.linalg.svd(C - mu, full_matrices=False)
v1 = Vt[0]
if spearmanr((C - mu) @ v1, birth).statistic < 0:
    v1 = -v1
expl = float(S[0] ** 2 / np.sum(S ** 2))
pc1 = (C - mu) @ v1
slope, icpt = np.polyfit(birth, pc1, 1)
res = pc1 - (slope * birth + icpt)
rho_pc1 = float(spearmanr(pc1, birth).statistic)

B = 1000
resb = np.zeros((B, len(keys)))
idxs = [np.where(y == k)[0] for k in keys]
for b in range(B):
    Cb = np.stack([Z[rng.choice(ix, len(ix))].mean(0) for ix in idxs])
    resb[b] = (Cb - mu) @ v1 - (slope * birth + icpt)  # mesmos eixos e mesma reta
lo, hi = np.percentile(resb, [2.5, 97.5], axis=0)
sig = (lo > 0) | (hi < 0)

SUR = [k.split(",")[0] for k in keys]
SHORT = [(k.split(",")[1].strip()[0] + ". " + s) if SUR.count(s) > 1 else s for k, s in zip(keys, SUR)]
tab = pd.DataFrame(dict(composer=keys, nome=SHORT, nascimento=birth.astype(int), periodo=meta.periodo.values,
                        n_pecas=[len(ix) for ix in idxs], pc1=pc1.round(4), residuo=res.round(4),
                        ic_lo=lo.round(4), ic_hi=hi.round(4), significativo=sig,
                        direcao=np.where(~sig, "", np.where(res > 0, "mais moderno que a data", "mais antigo que a data"))))
tab.sort_values("residuo", ascending=False).to_csv(HERE / "residuos_tempo.csv", index=False)

fig, ax = plt.subplots(figsize=(13, 8.5))
xs = np.linspace(birth.min() - 10, birth.max() + 10, 50)
ax.plot(xs, slope * xs + icpt, color="gray", lw=1.2, ls="--", zorder=1)
for i in range(len(keys)):
    c = COLORS.get(meta.periodo.values[i], "gray")
    if sig[i]:  # barra de IC do resíduo, desenhada em torno do ponto: reta + [lo, hi]
        yl, yh = slope * birth[i] + icpt + lo[i], slope * birth[i] + icpt + hi[i]
        ax.plot([birth[i]] * 2, [yl, yh], color=c, lw=2, zorder=2)
    ax.scatter(birth[i], pc1[i], s=30 + 1.5 * len(idxs[i]) ** 0.5 * 6, color=c, edgecolor="black" if sig[i] else "white",
               linewidth=1.2 if sig[i] else 0.6, zorder=3)
texts = [ax.text(birth[i], pc1[i], SHORT[i] + (" *" if sig[i] else ""), fontsize=8,
                 fontweight="bold" if sig[i] else "normal") for i in range(len(keys))]
adjust_text(texts, x=birth, y=pc1, ax=ax, arrowprops=dict(arrowstyle="-", color="gray", lw=0.4),
            expand=(1.3, 1.5), force_text=(0.4, 0.6), max_move=(60, 60))
for per, c in COLORS.items():
    ax.scatter([], [], color=c, label=per)
ax.legend(loc="upper left", fontsize=9, title="Período")
ax.set_xlabel("Ano de nascimento")
ax.set_ylabel(f"PC1 do mapa ({expl:.0%} da variância dos centróides)")
ax.set_title("O eixo principal do mapa segue a cronologia, mas alguns compositores fogem da reta\n"
             f"(Spearman PC1 × nascimento = {rho_pc1:.2f}".replace(".", ",") + f"; * e contorno preto = IC95% do resíduo exclui zero)", fontsize=12)
fig.tight_layout()
fig.savefig(HERE / "figs" / "tempo_vs_mapa.png", dpi=150)

pos = tab[tab.significativo & (tab.residuo > 0)].sort_values("residuo", ascending=False)
neg = tab[tab.significativo & (tab.residuo < 0)].sort_values("residuo")
out = dict(config=dict(layer=6, pooling="mean", windows=[1, 2], bootstrap=B), pc1_var_explicada=round(expl, 4),
           spearman_pc1_nascimento=round(rho_pc1, 4), reta=dict(inclinacao_por_ano=float(slope), intercepto=float(icpt)),
           r2_reta=round(float(1 - np.sum(res ** 2) / np.sum((pc1 - pc1.mean()) ** 2)), 4),
           mais_moderno_que_a_data=[dict(c=r.nome, residuo=r.residuo, ic=[r.ic_lo, r.ic_hi]) for r in pos.itertuples()],
           mais_antigo_que_a_data=[dict(c=r.nome, residuo=r.residuo, ic=[r.ic_lo, r.ic_hi]) for r in neg.itertuples()])
(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
