"""F14: compasso ou gênero? (H15). Camada 6, mean, janelas 1,2, peça, centrado, l2norm.
Valsas contra outras danças ternárias e danças binárias, dentro do compositor (parte 2)
e contra referências de Chopin (parte 3)."""
import itertools, json, os, re, sys
from pathlib import Path
os.environ["CV_WINDOWS"] = "1,2"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist

rng = np.random.default_rng(0)
CHO = "Chopin, Frédéric"
RX = dict(
    V=r"valse|valsa|waltz|walzer",
    T=r"menuet|minuet|minueto|mazur|polonaise|polacca|sarabande|ländler|landler",
    B=r"polka|polca|march|marche|marcha|galop|rag\b|tango|maxixe|schottisch|gavotte|bourr|two-step|cake ?walk")
X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Z = l2norm(center(Xp)[0])
D = cosine_dist(Z)
ck, ti = dp.composer_key.values, dp.title.values


def classify(t):
    for k in "VTB":  # valsa tem prioridade (ex.: "Mazurka-valse")
        if re.search(RX[k], t, re.I):
            return k
    return ""


cls = np.array([classify(t) for t in ti])
multi = [t for t in ti if sum(bool(re.search(RX[k], t, re.I)) for k in "VTB") > 1]
VAR = np.array([bool(re.search(r"variation", t, re.I)) for t in ti])  # "Variações sobre um minueto" não é minueto
cls_main = np.where(VAR, "", cls)
# MIDIs duplicados: peças com título diferente e vetor idêntico (mesmo compositor, perda idêntica).
# Cada grupo vira uma peça só se todos os títulos têm a mesma classe; grupos de classe mista ou sem classe saem.
_key = [(c, r.tobytes()) for c, r in zip(ck, np.round(Xp, 4))]
_grp = {}
for i, k in enumerate(_key):
    _grp.setdefault(k, []).append(i)
dup_groups = [g for g in _grp.values() if len(g) > 1]
cls_raw = cls_main.copy()
for g in dup_groups:
    cs = {cls_main[i] for i in g}
    for i in g[1:]:
        cls_main[i] = ""
    if len(cs) > 1 or "" in cs:
        cls_main[g[0]] = ""
n_dup_pecas = int(sum(len(g) for g in dup_groups))
n_dup_classif = int(sum(1 for g in dup_groups for i in g if cls[i] != ""))
NAME = dict(V="valsa", T="outras ternárias", B="binárias")

# ---------- 1. contagens
def tab(v, suf):
    t = pd.DataFrame(dict(composer=ck, classe=v)).query("classe != ''")
    t = pd.crosstab(t.composer, t.classe).reindex(columns=list("VTB"), fill_value=0)
    t.columns = [NAME[c] + suf for c in t.columns]
    return t
ct = tab(cls, " (regex)").join(tab(cls_main, " (únicas, usadas)"), how="outer").fillna(0).astype(int)
ct["total regex"] = ct.filter(like="(regex)").sum(axis=1)
ct["total usadas"] = ct.filter(like="usadas").sum(axis=1)
ct.loc["TOTAL"] = ct.sum()
ct.to_csv(HERE / "contagens.csv")
n_var_excl = int(((cls != "") & VAR).sum())

# ---------- 2. dentro do compositor
def pair_mean(idx_a, idx_b, same):
    sub = D[np.ix_(idx_a, idx_b)]
    if same:
        n = len(idx_a)
        if n < 2:
            return np.nan
        return sub[~np.eye(n, dtype=bool)].mean()
    return sub.mean()


def within(clsv, drop=()):
    rows = []
    for c in sorted(set(ck) - set(drop)):
        ix = {k: np.where((ck == c) & (clsv == k))[0] for k in "VTB"}
        if sum(len(v) > 0 for v in ix.values()) < 2:
            continue
        r = dict(composer=c, **{f"n_{k}": len(ix[k]) for k in "VTB"})
        for a, b in [("V", "V"), ("T", "T"), ("V", "T"), ("V", "B"), ("T", "B")]:
            r[a + b] = pair_mean(ix[a], ix[b], a == b) if len(ix[a]) and len(ix[b]) else np.nan
        rows.append(r)
    return pd.DataFrame(rows)


def paired(W, a, b, label):
    s = W[[a, b]].dropna()
    n = len(s)
    out = dict(comparacao=label, n_compositores=n, media_a=float(s[a].mean()) if n else None,
               media_b=float(s[b].mean()) if n else None)
    if n >= 5:
        d = (s[a] - s[b]).values
        out["dif_media"] = float(d.mean())
        out["dif_mediana"] = float(np.median(d))
        out["n_a_menor"] = int((d < 0).sum())
        out["p_bilateral"] = float(wilcoxon(d).pvalue)
        out["p_a_menor"] = float(wilcoxon(d, alternative="less").pvalue)
        bs = [rng.choice(d, n).mean() for _ in range(5000)]
        out["ic95_dif"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    return out


def tests(W):
    return [paired(W, "VT", "VB", "(a) V-T vs V-B"),
            paired(W, "TB", "VB", "(b) T-B vs V-B"),
            paired(W, "VV", "VT", "(c) V-V vs V-T"),
            paired(W, "VV", "VB", "(d) V-V vs V-B"),
            paired(W, "TT", "TB", "(e) T-T vs T-B")]


W = within(cls_main)
W.to_csv(HERE / "dentro_compositor.csv", index=False)
# conjunto completo: compositores com as três classes (V, T e B)
W3 = W[(W.n_V > 0) & (W.n_T > 0) & (W.n_B > 0)]
res2 = dict(todos=tests(W), tres_classes=tests(W3),
            sem_chopin=tests(W[W.composer != CHO]),
            regex_literal_sem_dedup=tests(within(cls)),  # sem tirar "Variations" nem duplicatas
            compositores_tres_classes=W3.composer.tolist())
# restrito às valsas excluindo T = mazurca/polonaise de Chopin (dominantes): só minueto/ländler/sarabande
cls_alt = cls_main.copy()
for i in range(len(ti)):
    if cls_alt[i] == "T" and re.search(r"mazur|polonaise|polacca", ti[i], re.I):
        cls_alt[i] = ""
res2["T_so_minueto_landler_sarabande"] = tests(within(cls_alt))

# ---------- 3. entre compositores: referências de Chopin
is_cho = ck == CHO
val_c = np.where(is_cho & (cls_main == "V"))[0]
maz_c = np.where(is_cho & (cls_main == "T") & np.array([bool(re.search("mazur", t, re.I)) for t in ti]))[0]
loo = lambda ref, i: Z[[j for j in ref if j != i]].mean(0)
cd = lambda z, c: 1 - float(z @ c / (np.linalg.norm(z) * np.linalg.norm(c) + 1e-12))


def sub(t, k):
    if k == "V": return "valsa"
    if k == "B": return "binária"
    if re.search("mazur", t, re.I): return "mazurca"
    if re.search("menuet|minuet|minueto", t, re.I): return "minueto"
    return "outra ternária"


rows = []
for i in np.where(cls_main != "")[0]:
    rows.append(dict(composer=ck[i], title=ti[i], subclasse=sub(ti[i], cls_main[i]),
                     d_valsaCho=cd(Z[i], loo(val_c, i)), d_mazCho=cd(Z[i], loo(maz_c, i)), chopin=bool(is_cho[i])))
P3 = pd.DataFrame(rows)
P3["dif"] = P3.d_valsaCho - P3.d_mazCho  # negativo = mais perto das valsas de Chopin
P3.to_csv(HERE / "entre_compositores.csv", index=False)
res3 = {}
for chopin in (False, True):
    G = P3[P3.chopin == chopin]
    for s, g in G.groupby("subclasse"):
        cm = g.groupby("composer")[["d_valsaCho", "d_mazCho", "dif"]].mean()
        r = dict(n_pecas=len(g), n_compositores=len(cm), d_valsaCho=float(g.d_valsaCho.mean()),
                 d_mazCho=float(g.d_mazCho.mean()), dif_pecas=float(g.dif.mean()),
                 dif_compositores=float(cm.dif.mean()), frac_pecas_mais_perto_valsa=float((g.dif < 0).mean()),
                 n_comp_mais_perto_valsa=int((cm.dif < 0).sum()))
        if len(cm) >= 5:
            r["p_wilcoxon_dif_compositores"] = float(wilcoxon(cm.dif).pvalue)
        res3[("Chopin(LOO)" if chopin else "outros") + ":" + s] = r

# minuetos clássicos: 2x2 (época x compasso), sem o próprio compositor
birth = load_meta().set_index("composer_key").birth.to_dict()
early = np.array([birth.get(c, 9999) <= 1800 for c in ck])
res3m = {}
rowsm = []
for comp in ["Mozart, Wolfgang Amadeus", "Bach, Johann Sebastian", "Beethoven, Ludwig van", "Handel, George Frideric"]:
    mi = np.where((ck == comp) & (cls_main == "T") & np.array([bool(re.search("menuet|minuet|minueto", t, re.I)) for t in ti]))[0]
    oth = ck != comp
    pools = dict(valsa_cedo=(cls_main == "V") & early & oth, valsa_tarde=(cls_main == "V") & ~early & oth,
                 bin_cedo=(cls_main == "B") & early & oth, bin_tarde=(cls_main == "B") & ~early & oth)
    r = dict(n_minuetos=len(mi))
    for k, m in pools.items():
        r[k] = float(D[np.ix_(mi, np.where(m)[0])].mean())
        r["n_" + k] = int(m.sum())
        r["ncomp_" + k] = int(len(set(ck[m])))
    r["efeito_compasso_cedo"] = r["bin_cedo"] - r["valsa_cedo"]    # >0: mais perto da valsa
    r["efeito_compasso_tarde"] = r["bin_tarde"] - r["valsa_tarde"]
    r["efeito_epoca_valsa"] = r["valsa_tarde"] - r["valsa_cedo"]   # >0: mais perto das valsas da própria época
    r["efeito_epoca_bin"] = r["bin_tarde"] - r["bin_cedo"]
    res3m[comp] = r
    rowsm.append(dict(composer=comp, **r))
pd.DataFrame(rowsm).to_csv(HERE / "minuetos_classicos.csv", index=False)

out = dict(config=dict(layer=6, pooling="mean", windows=[1, 2], n_pecas=len(dp)),
           contagem_classes={NAME[k]: int((cls == k).sum()) for k in "VTB"}, titulos_em_mais_de_uma_regex=multi,
           pecas_variacoes_excluidas=n_var_excl, midis_duplicados=dict(grupos=len(dup_groups), pecas=n_dup_pecas, pecas_com_classe_regex=n_dup_classif, pecas_usadas_apos_dedup={NAME[k]: int((cls_main == k).sum()) for k in 'VTB'}),
           parte2_dentro_compositor=res2, parte3_chopin=res3, parte3_minuetos=res3m,
           ref_chopin=dict(n_valsas=len(val_c), n_mazurcas=len(maz_c)))
(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))

# ---------- figura
Wf = W3.copy()
Wf["lab"] = [c.split(",")[0] + f" ({a}/{b}/{d})" for c, a, b, d in zip(Wf.composer, Wf.n_V, Wf.n_T, Wf.n_B)]
Wf = Wf.sort_values("VB")
fig, axs = plt.subplots(1, 2, figsize=(14, 6.8), gridspec_kw=dict(width_ratios=[1.25, 1]))
ax = axs[0]
cs = dict(VV="#1f77b4", VT="#2ca02c", TB="#9467bd", VB="#d62728")
lb = dict(VV="valsa–valsa", VT="valsa–outra ternária", TB="outra ternária–binária", VB="valsa–binária")
y = np.arange(len(Wf))
for k in ["VV", "VT", "TB", "VB"]:
    ax.scatter(Wf[k], y, c=cs[k], s=45, label=lb[k], zorder=3)
for i, (_, r) in enumerate(Wf.iterrows()):
    v = [r[k] for k in ["VV", "VT", "TB", "VB"] if not np.isnan(r[k])]
    ax.hlines(i, min(v), max(v), color="0.8", zorder=1)
ax.set_yticks(y); ax.set_yticklabels(Wf.lab, fontsize=9)
for k in ["VT", "TB", "VB"]:
    ax.axvline(W3[k].mean(), color=cs[k], ls=":", lw=1.2, alpha=.8)
ax.set_xlabel("distância cosseno média entre peças do mesmo compositor")
ax.set_title("A. Dentro do compositor, 10 compositores com as 3 classes (n valsas/ternárias/binárias)\npontilhadas: média dos compositores", fontsize=10)
ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
ax = axs[1]
order = ["valsa", "minueto", "outra ternária", "mazurca", "binária"]
G = P3[~P3.chopin]
for j, s in enumerate(order):
    g = G[G.subclasse == s]
    ax.scatter(g.dif, rng.normal(j, 0.07, len(g)), s=12, alpha=.35, c="0.4", zorder=2)
    cm = g.groupby("composer").dif.mean()
    ax.scatter(cm, np.full(len(cm), j), s=55, c="#e8a33d", edgecolor="k", zorder=3)
ax.axvline(0, color="k", lw=1)
ax.set_yticks(range(len(order)))
ax.set_yticklabels([f"{s}\n{(G.subclasse == s).sum()} peças, {G[G.subclasse == s].composer.nunique()} comp." for s in order], fontsize=9)
ax.invert_yaxis()
ax.set_xlabel("d(valsas de Chopin) − d(mazurcas de Chopin)\n← mais perto das valsas        mais perto das mazurcas →")
ax.set_title("B. Peças de outros compositores contra Chopin\ncinza: peças; laranja: média por compositor", fontsize=10)
t = res2["tres_classes"]
fig.suptitle("As valsas se agrupam entre si, mas outras danças ternárias não ficam mais perto delas do que as binárias:\n"
             "o agrupamento parece ser da valsa, e não só do compasso (exploratório, n pequeno)", fontsize=12, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(HERE / "figs" / "compasso.png", dpi=140)
print(json.dumps(out, indent=1, ensure_ascii=False))
