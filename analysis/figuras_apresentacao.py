"""Figuras para apresentação (só leitura de CSV/JSON e dos .npz; não usa o modelo).

a) F3_geometria/figs/mapa_apresentacao.png  - mesma PCA de F3/run.py (SVD dos centróides centrados),
   usando só a janela 1 (passada 1), como no metrics.json da F3, mesmo que já existam janelas novas.
   O sinal do PC1 é invertido se preciso, para o tempo crescer para a direita (cosmético).
b) F7_deslocamento/figs/steering.png
c) F2_representacao/figs/camadas.png
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

INK, MUTED = "#222222", "#666666"
PC = {"Renascimento": "#8c564b", "Barroco": "#d62728", "Clássico": "#ff7f0e", "Romântico": "#1f77b4", "Moderno": "#2ca02c"}
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def mapa():
    cfg = json.loads((HERE / "F2_representacao/metrics.json").read_text())["best"]
    L, P = cfg["layer"], cfg["pooling"]
    X, df = load(L, P, windows=(1,))
    Xp, dp = piece_level(X, df)
    Xc, mu = center(Xp)
    Z = l2norm(Xc)
    C, keys = centroids(Z, dp)
    D = cosine_dist(C)
    n_by = dp.composer_key.value_counts()
    meta = load_meta().set_index("composer_key").loc[keys]
    U, S, Vt = np.linalg.svd(C - C.mean(0), full_matrices=False)
    P2 = (C - C.mean(0)) @ Vt[:2].T
    expl = (S ** 2 / np.sum(S ** 2))[:2]
    iu = np.triu_indices(len(keys), 1)
    D2 = np.linalg.norm(P2[:, None] - P2[None], axis=-1)
    dist = spearmanr(D[iu], D2[iu]).statistic
    rho_pc1 = spearmanr(P2[:, 0], meta.birth.values.astype(float), nan_policy="omit").statistic
    flip = -1 if rho_pc1 < 0 else 1
    P2[:, 0] *= flip
    rho1 = spearmanr(P2[:, 0], meta.birth.values.astype(float), nan_policy="omit").statistic
    rho2 = spearmanr(P2[:, 1], meta.birth.values.astype(float), nan_policy="omit").statistic
    print(f"n={len(keys)} pecas={len(dp)} expl={expl.round(4)} distorcao={dist:.4f} rho(PC1,nasc)={rho1:.3f} rho(PC2,nasc)={rho2:.3f} flip={flip}")
    fig, ax = plt.subplots(figsize=(14, 9.5))
    texts, manual = [], []
    sc = []
    for i, k in enumerate(keys):
        sc.append(ax.scatter(*P2[i], s=30 + 3.5 * n_by[k], color=PC.get(meta.periodo.values[i], "gray"), alpha=0.85,
                   edgecolor="white", linewidth=1.2, zorder=3))
        sob = k.split(",")[0]
        lab = {"Scott, James": "J. Scott", "Scott, Cyril": "C. Scott"}.get(k, sob)
        (manual if sob in ('Bach', 'Johnson', 'Alkan') else texts).append(ax.text(*P2[i], lab, fontsize=10, color=INK, zorder=4))
    Xe, de = load(L, P, windows=(1,), include_extra=True)
    tt = de.composer_key.str.startswith("Abreu").values
    pts = [t.get_position() for t in texts]
    if tt.any():
        zt = l2norm(Xe[tt].mean(0, keepdims=True) - mu)
        pt = ((zt - C.mean(0)) @ Vt[:2].T)[0]
        pt[0] *= flip
        ax.scatter(*pt, marker="*", s=420, color="black", edgecolor="white", zorder=5)
        texts.append(ax.text(*pt, "Tico-Tico", fontsize=11, fontweight="bold", color="black", zorder=6))
    adjust_text(texts, x=P2[:, 0], y=P2[:, 1], ax=ax, expand=(1.3, 1.7),
                arrowprops=dict(arrowstyle="-", color="#999999", lw=0.6), max_move=None, iter_lim=1000)
    xr = np.ptp(P2[:, 0]); yr = np.ptp(P2[:, 1])
    for t in manual:  # ajuste manual dos rótulos que caem sobre o próprio ponto
        i = [k.split(",")[0] for k in keys].index(t.get_text()) if t.get_text() in [k.split(",")[0] for k in keys] else None
        if t.get_text() in ("Bach", "Johnson", "Alkan"):
            x0, y0 = P2[i]
            dx, dy = {"Bach": (0.035, -0.03), "Johnson": (-0.012, 0.0), "Alkan": (-0.03, 0.045)}[t.get_text()]
            t.set_position((x0 + dx * xr, y0 + dy * yr))
            if t.get_text() == "Alkan":
                ax.plot([x0, x0 + dx * xr * 0.9], [y0, y0 + dy * yr * 0.8], color="#999999", lw=0.6, zorder=2)
            if t.get_text() == "Bach":
                ax.plot([x0, x0 + dx * xr * 0.9], [y0, y0 + dy * yr * 0.8], color="#999999", lw=0.6, zorder=2)
            t.set_ha("right" if t.get_text() in ("Johnson", "Alkan") else "left"); t.set_va("center")
    for per, c in PC.items():
        ax.scatter([], [], color=c, s=90, label=per)
    ax.scatter([], [], marker="*", s=200, color="black", label="Tico-Tico no Fubá (Abreu)")
    ax.legend(loc="upper right", fontsize=10, frameon=False, title="Período (cor)  ·  nº de peças (tamanho)")
    ax.set_xlabel(f"PC1 ({expl[0]:.0%} da variância dos centróides) · mais antigo à esquerda", color=MUTED)
    ax.set_ylabel(f"PC2 ({expl[1]:.0%})", color=MUTED)
    ax.set_title("O eixo principal do mapa acompanha a cronologia", fontsize=17, loc="left", fontweight="bold", pad=22)
    ax.text(0, 1.015, f"Centróides de {len(keys)} compositores, modelo AMT, camada {L}, pooling {P}. "
            f"Distorção da projeção: Spearman {dist:.2f}.", transform=ax.transAxes, fontsize=10, color=MUTED)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    out = HERE / "F3_geometria/figs/mapa_apresentacao.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)


def steering():
    d = pd.read_csv(HERE / "F7_deslocamento/steering_forte.csv")
    order = [("nenhum", "sem\nsteering"), ("aleatorio", "vetor\naleatório"), ("centrado", "vetor centrado\n(Chopin)"),
             ("caminho_t0", "caminho\nt = 0 (Bach)"), ("caminho_t0.5", "caminho\nt = 0,5"), ("caminho_t1", "caminho\nt = 1 (Chopin)")]
    g = d.groupby("cond").progresso.agg(["mean", "std", "count"])
    g["se"] = g["std"] / np.sqrt(g["count"])
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(order))
    for j, (c, _) in enumerate(order):
        col = "#1f77b4" if c in ("centrado", "caminho_t1") else "#888888"
        ax.errorbar(j, g.loc[c, "mean"], yerr=g.loc[c, "se"], fmt="o", ms=10, color=col, ecolor=col, capsize=5, lw=2,
                    markeredgecolor="white", zorder=3)
        ax.text(j + 0.12, g.loc[c, "mean"], f"{g.loc[c, 'mean']:.2f}", va="center", fontsize=11, color=INK)
    ax.axhline(0, color=MUTED, lw=1, ls="--"); ax.axhline(1, color=MUTED, lw=1, ls="--")
    ax.text(len(order) - 0.45, 0.015, "origem (centróide de Bach)", ha="right", va="bottom", fontsize=10, color=MUTED)
    ax.text(len(order) - 0.45, 0.985, "alvo (centróide de Chopin)", ha="right", va="top", fontsize=10, color=MUTED)
    ax.set_xticks(x); ax.set_xticklabels([l for _, l in order], fontsize=10)
    ax.set_ylim(-0.1, 1.1); ax.set_xlim(-0.5, len(order) - 0.4)
    ax.set_ylabel("progresso na direção Bach → Chopin")
    n = int(g["count"].iloc[0])
    ax.set_title("Somar o vetor de Chopin leva a música para o lado de Chopin; um vetor aleatório não", fontsize=14,
                 loc="left", fontweight="bold", pad=24)
    ax.text(0, 1.02, f"Média ± erro padrão, n = {n} continuações por condição (7 sementes de Bach × 2), α = 1, camada 6. "
            "Progresso relido sem steering.", transform=ax.transAxes, fontsize=9.5, color=MUTED)
    fig.tight_layout()
    fig.savefig(HERE / "F7_deslocamento/figs/steering.png", dpi=150)
    plt.close(fig)


def camadas():
    m = json.loads((HERE / "F2_representacao/metrics.json").read_text())
    r = pd.DataFrame(m["results"])
    fig, ax = plt.subplots(figsize=(10, 6))
    for pool, col, lab in [("mean", "#1f77b4", "média da janela"), ("last", "#d62728", "último token")]:
        s = r[r.pooling == pool].sort_values("layer")
        ax.plot(s.layer, s.bal_acc, "o-", color=col, lw=2, ms=7, markeredgecolor="white", label=lab)
        k = s.loc[s.bal_acc.idxmax()]
        ax.annotate(f"melhor: camada {int(k.layer)} ({k.bal_acc:.2f})", (k.layer, k.bal_acc), xytext=(0, 12),
                    textcoords="offset points", ha="center", fontsize=10, color=INK)
    ax.axhline(m["chance"], color=MUTED, ls="--", lw=1)
    ax.text(12.1, m["chance"] + 0.006, f"acaso = 1/52 = {m['chance']:.3f}", ha="right", fontsize=10, color=MUTED)
    ax.set_xticks(range(13)); ax.set_xlabel("camada (0 = embeddings, 12 = última)")
    ax.set_ylabel("acurácia balanceada (validação cruzada, 5 dobras)")
    ax.set_ylim(0, 0.36); ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1, 0.9))
    ax.set_title("As camadas do meio separam melhor os compositores que a última", fontsize=14, loc="left",
                 fontweight="bold", pad=24)
    ax.text(0, 1.02, "2.183 peças, 52 compositores, regressão logística, espaço centrado.", transform=ax.transAxes,
            fontsize=9.5, color=MUTED)
    fig.tight_layout()
    fig.savefig(HERE / "F2_representacao/figs/camadas.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    for f in (HERE / "F2_representacao/figs", HERE / "F7_deslocamento/figs"):
        f.mkdir(exist_ok=True)
    camadas(); steering(); mapa()
