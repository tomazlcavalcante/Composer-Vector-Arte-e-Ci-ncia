import json, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
H = "."
pares = [("Bach → Chopin", "descritores_steering.csv", "descritores_ref.csv", "Bach", "Chopin"),
         ("Mozart → Debussy", "descritores_steering_Mozart_Debussy.csv", "descritores_ref_Mozart_Debussy.csv", "Mozart", "Debussy"),
         ("Chopin → Joplin", "descritores_steering_Chopin_Joplin.csv", "descritores_ref_Chopin_Joplin.csv", "Chopin", "Joplin")]
mets = [("dur_media_s", "Duração média das notas (s)"), ("notas_por_s", "Notas por segundo")]
fig, axs = plt.subplots(1, 2, figsize=(10, 4.8))
for ax, (m, tit) in zip(axs, mets):
    for i, (nome, fs, fr, s, t) in enumerate(pares):
        d = pd.read_csv(fs); r = pd.read_csv(fr)
        w = d.groupby(["seed", "cond"])[m].mean().unstack()
        diff = (w["centrado"] - w["nenhum"]).dropna()
        mu, se = diff.mean(), diff.std(ddof=1) / np.sqrt(len(diff))
        ref = r.groupby("composer")[m].mean()
        exp = np.sign(ref.filter(like=t).iloc[0] - ref.filter(like=s).iloc[0])
        ax.errorbar(i, mu, yerr=se, fmt="o", color="#2a6f97", capsize=5, ms=8)
        ax.annotate(f"{mu:+.2f}".replace(".", ","), (i, mu), xytext=(12, -3), textcoords="offset points", fontsize=9, color="#2a6f97")
        y0 = 0.5 if exp > 0 else -0.5
        ax.annotate("", xy=(i - 0.28, 0), xytext=(i - 0.28, 0),)
        ax.annotate("", xy=(i - 0.3, exp * 0.0), xytext=(i - 0.3, 0))
        ax.text(i, 1.0, "esperado\n" + ("▲" if exp > 0 else "▼"), transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=9, color="#b5483a")
    ax.axhline(0, color="#999", lw=.8)
    ax.set_xticks(range(3)); ax.set_xticklabels([p[0] for p in pares]); ax.set_xlim(-.6, 2.6)
    ax.set_title(tit, fontsize=11, loc="left")
    ax.set_ylabel("centrado − nenhum (média ± EP, 7 sementes)", fontsize=9)
    lo, hi = ax.get_ylim(); ax.set_ylim(lo, hi + (hi - lo) * 0.25)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.suptitle("Efeito do vetor centrado: a duração sobe em dois pares, e em Joplin não; notas/s segue o alvo só em Joplin", fontsize=11.5, x=0.02, ha="left")
fig.text(0.02, 0.01, "▲/▼ = direção do alvo na referência (média do alvo − média da origem). Mudanças pareadas por semente (média das 2 amostras).", fontsize=8, color="#555")
fig.tight_layout(rect=(0, 0.04, 1, 0.94))
fig.savefig("figs/descritores_tres_pares.png", dpi=150)
