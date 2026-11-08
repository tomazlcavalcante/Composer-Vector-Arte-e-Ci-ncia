"""F13 / H14 (exploratória): valsas verificadas de Nazareth e valsas de ragtime, com eixo único.
Centróide do ragtime SEM as 4 valsas de ragtime. Camada 6, mean, janelas 1,2, piece_level, center, l2norm."""
import json, os, sys
from pathlib import Path
os.environ["CV_WINDOWS"] = "1,2"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from adjustText import adjust_text

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, piece_level, center, l2norm

NAZ, CHO = "Nazareth, Ernesto", "Chopin, Frédéric"
RAG = ["Joplin, Scott", "Scott, James", "Johnson, Charles Leslie"]
X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp)
Z = l2norm(Xc)
ck, ti = dp.composer_key.values, dp.title.values
unit = lambda v: v / (np.linalg.norm(v) + 1e-12)
cd = lambda z, c: 1 - float(unit(z) @ unit(c))

gen = pd.read_csv(HERE / "nazareth_generos_verificados.csv")
gen = gen[gen.grupo == "Nazareth"].set_index("title").genero_verificado.to_dict()
rv = pd.read_csv(HERE / "ragtime_valsas.csv")
wal_titles = set(rv[rv.valsa].title)
rag_idx = np.where(np.isin(ck, RAG))[0]
is_w = np.array([ti[i] in wal_titles for i in rag_idx])
assert is_w.sum() == 4
rag_nw = rag_idx[~is_w]; rag_w = rag_idx[is_w]
cent_rag = Z[rag_nw].mean(0)
cho_c = Z[ck == CHO].mean(0)

rows = []
for i in np.where(ck == NAZ)[0]:
    g = gen.get(ti[i], "não verificado")
    rows.append(dict(serie="Nazareth", title=ti[i], genero=g, d_rag=cd(Z[i], cent_rag), d_cho=cd(Z[i], cho_c)))
for i in rag_idx:
    w = i in rag_w
    c = Z[rag_nw[rag_nw != i]].mean(0)
    rows.append(dict(serie="valsa ragtime" if w else "rag", title=ti[i], genero="valsa" if w else "", d_rag=cd(Z[i], c), d_cho=cd(Z[i], cho_c)))
Xe, de = load(6, "mean", windows=(1, 2), include_extra=True)
tt = de.composer_key.str.startswith("Abreu").values
zt = l2norm(Xe[tt].mean(0, keepdims=True) - mu)[0]
rows.append(dict(serie="Tico-Tico", title="Tico-Tico", genero="", d_rag=cd(zt, cent_rag), d_cho=cd(zt, cho_c)))
R = pd.DataFrame(rows); R.to_csv(HERE / "valsas_distancias.csv", index=False)

N = R[R.serie == "Nazareth"]
nv = N[N.genero == "valsa"]; nt = N[N.genero == "tango/polca"]
mw = lambda a, b, alt: mannwhitneyu(a, b, alternative=alt)
m = {}
m["nazareth_valsas"] = dict(n=len(nv), d_rag=nv.d_rag.mean(), d_cho=nv.d_cho.mean(), titles=nv.title.tolist())
m["nazareth_tango_polca"] = dict(n=len(nt), d_rag=nt.d_rag.mean(), d_cho=nt.d_cho.mean())
m["nv_vs_nt_rag_p_greater"] = mw(nv.d_rag, nt.d_rag, "greater").pvalue
m["nv_vs_nt_cho_p_less"] = mw(nv.d_cho, nt.d_cho, "less").pvalue
m["nv_vs_nt_rag_U"] = mw(nv.d_rag, nt.d_rag, "greater").statistic
m["nv_vs_nt_rag_sep_min_valsa_vs_max_tango"] = (nv.d_rag.min(), nt.d_rag.max())
m["nv_vs_nt_cho_sep_max_valsa_vs_min_tango"] = (nv.d_cho.max(), nt.d_cho.min())
# sem Rosa Maria
nv3 = nv[nv.title != "Rosa Maria"]
m["sem_rosa_maria"] = dict(p_rag=mw(nv3.d_rag, nt.d_rag, "greater").pvalue, p_cho=mw(nv3.d_cho, nt.d_cho, "less").pvalue)
rw = R[R.serie == "valsa ragtime"]; rr = R[R.serie == "rag"]
m["ragtime_valsas"] = dict(n=len(rw), d_rag=rw.d_rag.mean(), d_cho=rw.d_cho.mean())
m["rags"] = dict(n=len(rr), d_rag=rr.d_rag.mean(), d_cho=rr.d_cho.mean())
m["rw_vs_rr_cho_p_less"] = mw(rw.d_cho, rr.d_cho, "less").pvalue
m["rw_vs_rr_rag_p_greater"] = mw(rw.d_rag, rr.d_rag, "greater").pvalue
m["tico_tico"] = R[R.serie == "Tico-Tico"][["d_rag", "d_cho"]].iloc[0].to_dict()
m["nao_verificado_n"] = int((N.genero == "não verificado").sum())
m["fado"] = N[N.genero == "fado"][["title", "d_rag", "d_cho"]].iloc[0].to_dict()
(HERE / "valsas_metrics.json").write_text(json.dumps(m, indent=1, ensure_ascii=False, default=float))
print(json.dumps(m, indent=1, ensure_ascii=False, default=float))

fig, ax = plt.subplots(figsize=(10, 7.5))
def sc(d, **k): ax.scatter(d.d_rag, d.d_cho, **k)
sc(rr, s=14, c="#c9c9c9", alpha=.7, label=f"rags (n={len(rr)})", zorder=1)
sc(N[N.genero.isin(["não verificado", "fado"])], s=30, c="#b0b0b0", marker="o", edgecolor="#8a8a8a", lw=.5,
   label=f"Nazareth, gênero não verificado (n={(N.genero.isin(['não verificado','fado'])).sum()}, inclui Ferramenta, fado)", zorder=2)
sc(nt, s=60, c="#d95f02", marker="s", edgecolor="k", lw=.6, label=f"Nazareth, tangos e polcas (n={len(nt)})", zorder=3)
sc(nv, s=110, c="#1b4f9c", marker="o", edgecolor="k", lw=1, label=f"Nazareth, valsas (n={len(nv)})", zorder=4)
sc(rw, s=110, c="#7b3294", marker="D", edgecolor="k", lw=1, label=f"valsas de ragtime (n={len(rw)})", zorder=4)
t = R[R.serie == "Tico-Tico"]
sc(t, s=330, c="gold", marker="*", edgecolor="k", label="Tico-Tico (Abreu)", zorder=5)
off = {"Harmony Club Waltz": (-12, 22, "right"), "Augustan Club Waltz": (-28, -34, "right"),
       "Binks' Waltz": (-18, 22, "right"), "Wedding of the Fairies Waltz": (22, 20, "left"),
       "Confidências": (-6, 26, "center"), "Rosa Maria": (14, 44, "center"),
       "Resignação": (4, 26, "center"), "Coração que sente": (-20, 24, "center")}
for r in pd.concat([nv, rw]).itertuples():
    dx, dy, ha = off[r.title]
    ax.annotate(r.title, (r.d_rag, r.d_cho), xytext=(dx, dy), textcoords="offset points", ha=ha, fontsize=9, weight="bold",
                color="#1b4f9c" if r.serie == "Nazareth" else "#7b3294",
                arrowprops=dict(arrowstyle="-", color="#555", lw=.6), zorder=6)
ax.set_xlabel("distância ao ragtime (cosseno, centróide dos rags sem valsas)")
ax.set_ylabel("distância a Chopin (cosseno)")
ax.set_title("Para o modelo, valsas de Nazareth e de Joplin soam mais perto de Chopin\nque dos seus próprios tangos e rags", fontsize=13)
ax.legend(fontsize=8, loc="upper right", framealpha=.9)
ax.grid(alpha=.2); ax.set_xlim(0.02, 1.4); ax.set_ylim(0.3, 1.5)
fig.text(.01, .005, "Camada 6, mean, 2 janelas; espaço centrado e normalizado. Centróide do ragtime = 79 rags (Joplin, J. Scott, Johnson) sem as 4 valsas; rags: sem a própria peça.\n"
         "Gêneros de Nazareth verificados em fontes externas para 13 de 22 peças (Rosa Maria: fonte comercial). Exploratório.", fontsize=7.5, color="#444", va="bottom")
fig.tight_layout(rect=(0, .05, 1, 1)); fig.savefig(HERE / "figs" / "valsas.png", dpi=150)
