"""F13 / C3: o fio brasileiro. H14: tangos/maxixes de Nazareth ficam mais perto do ragtime que as valsas.
Camada 6, mean, 2 janelas (1,2), centrado e normalizado como na F3. Exploratório."""
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import mannwhitneyu  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, piece_level, center, l2norm  # noqa: E402

(HERE / "figs").mkdir(exist_ok=True)
NAZ, VL, CHO = "Nazareth, Ernesto", "Villa-Lobos, Heitor", "Chopin, Frédéric"
RAG = ["Joplin, Scott", "Scott, James", "Johnson, Charles Leslie"]  # Scott, James (não Cyril Scott)

X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp)
Z = l2norm(Xc)
ck = dp.composer_key.values

def unit(v):
    return v / (np.linalg.norm(v) + 1e-12)

def cdist(z, c):
    return 1 - float(unit(z) @ unit(c))

def classify(t):
    tl = t.lower()
    if re.search(r"tango|maxixe|choro", tl):
        return "tango/maxixe/choro"
    if re.search(r"valse|valsa|waltz", tl):
        return "valsa"
    return "outro"

rag_idx = np.where(np.isin(ck, RAG))[0]
cho_c = Z[ck == CHO].mean(0)
rows = []
def add(i, grupo, Zi=None, own_rag=False):
    z = Z[i] if Zi is None else Zi
    ri = rag_idx[rag_idx != i] if own_rag else rag_idx
    r = dict(grupo=grupo, composer=ck[i] if Zi is None else "Abreu, Zequinha",
             title=dp.title.values[i] if Zi is None else "Tico-Tico no fubá",
             classe=classify(dp.title.values[i]) if Zi is None else "",
             d_ragtime=cdist(z, Z[ri].mean(0)), d_chopin=cdist(z, cho_c if ck[i] != CHO or Zi is not None
                                                          else Z[(ck == CHO) & (np.arange(len(ck)) != i)].mean(0)))
    return r

naz_idx = np.where(ck == NAZ)[0]
for i in naz_idx:
    r = add(i, "Nazareth")
    oth = naz_idx[naz_idx != i]
    r["d_nazareth_loo"] = cdist(Z[i], Z[oth].mean(0))
    rows.append(r)
for i in np.where(ck == VL)[0]:
    rows.append(add(i, "Villa-Lobos"))
for i in rag_idx:
    rows.append(add(i, "ragtime (ref.)", own_rag=True))
# Tico-Tico
Xe, de = load(6, "mean", windows=(1, 2), include_extra=True)
tt = de.composer_key.str.startswith("Abreu").values
tt_n = 0
if tt.any():
    zt = l2norm((Xe[tt].mean(0, keepdims=True) - mu))[0]
    r = add(0, "Tico-Tico", Zi=zt); r["d_nazareth_loo"] = cdist(zt, Z[naz_idx].mean(0)); rows.append(r)
    tt_n = int(de[tt].piece_id.nunique())
R = pd.DataFrame(rows)
R["d_ragtime_menos_chopin"] = R.d_ragtime - R.d_chopin
R.to_csv(HERE / "pecas.csv", index=False)
R[R.grupo == "Nazareth"][["title", "classe"]].to_csv(HERE / "nazareth_classes.csv", index=False)

m = dict(layer=6, pooling="mean", windows=[1, 2], ragtime_composers=RAG, n_ragtime_pieces=int(len(rag_idx)),
         n_tico_tico_pieces=tt_n)
nz = R[R.grupo == "Nazareth"]
m["nazareth_classes"] = nz.classe.value_counts().to_dict()
m["nazareth_titulos_tango_valsa"] = {c: nz[nz.classe == c].title.tolist() for c in ("tango/maxixe/choro", "valsa")}
def summ(s):
    return dict(n=int(len(s)), d_ragtime=float(s.d_ragtime.mean()), d_chopin=float(s.d_chopin.mean()),
                d_rag_minus_chopin=float(s.d_ragtime_menos_chopin.mean()),
                frac_mais_perto_ragtime_que_chopin=float((s.d_ragtime < s.d_chopin).mean()))
m["resumo"] = {g: summ(s) for g, s in R.groupby("grupo")}
for c, s in nz.groupby("classe"):
    m["resumo"][f"Nazareth/{c}"] = summ(s)
a = nz[nz.classe == "tango/maxixe/choro"].d_ragtime.values
b = nz[nz.classe == "valsa"].d_ragtime.values
if len(a) >= 2 and len(b) >= 2:
    m["H14_mannwhitney"] = dict(n_tango=len(a), n_valsa=len(b), p_less=float(mannwhitneyu(a, b, alternative="less").pvalue),
                                U=float(mannwhitneyu(a, b, alternative="less").statistic))
else:
    m["H14_mannwhitney"] = dict(n_tango=int(len(a)), n_valsa=int(len(b)),
                                nota="teste impossível: classes por título quase vazias")
# Nazareth inteiro: mais perto de Nazareth (LOO) que do ragtime?
m["nazareth_dist_LOO_media"] = float(nz.d_nazareth_loo.mean())
m["tico_tico"] = R[R.grupo == "Tico-Tico"][["d_ragtime", "d_chopin", "d_nazareth_loo"]].to_dict("records")
# Villa-Lobos: ordem entre os grupos
vl = R[R.grupo == "Villa-Lobos"]
m["villa_lobos_mais_perto_ragtime_que_nazareth"] = float(vl.d_ragtime.mean() - nz.d_ragtime.mean())
# Nazareth vs. ragtime: posição das peças de Nazareth entre todos os compositores (distância ao ragtime)
alld = []
for k in sorted(set(ck)):
    if k in RAG:
        continue
    alld.append((k, cdist(Z[ck == k].mean(0), Z[rag_idx].mean(0))))
alld.sort(key=lambda t: t[1])
m["ranking_compositores_por_dist_ao_ragtime"] = dict(
    posicao_nazareth=[k for k, _ in alld].index(NAZ) + 1, posicao_villa_lobos=[k for k, _ in alld].index(VL) + 1,
    n=len(alld), mais_proximos=[(k, round(d, 3)) for k, d in alld[:6]])
(HERE / "metrics.json").write_text(json.dumps(m, indent=1, ensure_ascii=False))

fig, ax = plt.subplots(figsize=(8.5, 7))
sty = {"ragtime (ref.)": ("#7f7f7f", "o", 25, "ragtime (Joplin, J. Scott, Johnson)"),
       "Villa-Lobos": ("#2ca02c", "s", 40, "Villa-Lobos"), }
for g, (c, mk, s, lab) in sty.items():
    d = R[R.grupo == g]; ax.scatter(d.d_ragtime, d.d_chopin, c=c, marker=mk, s=s, alpha=.65, label=lab)
for cl, c, lab in (("tango/maxixe/choro", "#d62728", "Nazareth: tango/maxixe/choro (título)"),
                   ("valsa", "#1f77b4", "Nazareth: valsa (título)"), ("outro", "#ff7f0e", "Nazareth: outro")):
    d = nz[nz.classe == cl]
    if len(d):
        ax.scatter(d.d_ragtime, d.d_chopin, c=c, s=55, edgecolor="k", label=f"{lab} (n={len(d)})")
d = R[R.grupo == "Tico-Tico"]
ax.scatter(d.d_ragtime, d.d_chopin, marker="*", s=350, c="gold", edgecolor="k", label="Tico-Tico (Abreu)", zorder=5)
ax.set_xlabel("distância cosseno ao centróide do ragtime"); ax.set_ylabel("distância cosseno ao centróide de Chopin")
ax.set_title("C3: fio brasileiro (camada 6, mean, 2 janelas)\nragtime sem a própria peça"); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(HERE / "figs" / "brasil.png", dpi=140)
print(json.dumps(m, indent=1, ensure_ascii=False)); print(nz[["title", "classe", "d_ragtime", "d_chopin"]].round(3).to_string())
