"""F17 - H21: o opus acompanha a posição no eixo do tempo (PC1) dentro da carreira?"""
import json, re, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import spearmanr, binomtest
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(21); NPERM = 5000; MIN_N = 8
# --- mesma PCA do D1_explorador/export.py (camada 6, mean, janelas 1,2, sem duplicatas)
X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp); Z = l2norm(Xc)
C, keys = centroids(Z, dp); Cm = C.mean(0)
U, S, Vt = np.linalg.svd(C - Cm, full_matrices=False)
meta = load_meta().set_index("composer_key")
birth = meta.loc[keys, "birth"].values.astype(float)
if np.corrcoef((C - Cm) @ Vt[0], birth)[0, 1] < 0: Vt[0] *= -1
Pp = (Z - Cm) @ Vt[:2].T
dp["pc1"] = Pp[:, 0]
expl = float((S**2 / (S**2).sum())[0])

# --- opus
def opus(t):
    if re.search(r"Op\.\s*posth", t, re.I): return None
    m = re.search(r"\bOp(?:\.|us)\s*(\d+)", t, re.I)
    return int(m.group(1)) if m else None
dp["opus"] = dp.title.map(opus)

ALVOS = ["Scriabin, Aleksandr", "Beethoven, Ludwig van", "Brahms, Johannes", "Schumann, Robert", "Rachmaninoff, Sergei",
         "Prokofiev, Sergey", "Fauré, Gabriel", "Grieg, Edvard", "Medtner, Nikolay", "Chopin, Frédéric", "Mendelssohn, Felix"]
LIM = {"Chopin, Frédéric": 65, "Mendelssohn, Felix": 72}
PROX = {"Beethoven, Ludwig van": "Romântico", "Scriabin, Aleksandr": "Moderno"}
per = meta.periodo
sub = dp[dp.composer_key.isin(ALVOS) & dp.opus.notna()].copy()
for k, lim in LIM.items(): sub = sub[~((sub.composer_key == k) & (sub.opus > lim))]
sub["opus"] = sub.opus.astype(int)

def perm_p(x, y, stat):
    obs = stat(x, y)
    nulls = np.array([stat(rng.permutation(x), y) for _ in range(NPERM)])
    return obs, (1 + np.sum(np.abs(nulls) >= abs(obs))) / (NPERM + 1), (1 + np.sum(nulls >= obs)) / (NPERM + 1)
rho = lambda a, b: spearmanr(a, b)[0]

rows, nulls_w = [], {}
for k in ALVOS:
    s = sub[sub.composer_key == k]
    if len(s) < MIN_N:
        print("excluído (n<8):", k, len(s)); continue
    r, p2, p1 = perm_p(s.opus.values, s.pc1.values, rho)
    # distância ao centróide do período seguinte (ou do próprio), sem o compositor
    alvo_per = PROX.get(k, per[k])
    ks = [c for c in keys if per[c] == alvo_per and c != k]
    cen = Z[dp.composer_key.isin(ks).values].mean(0, keepdims=True)
    d = cosine_dist(Z[s.index.values], cen)[:, 0]
    r2, q2, _ = perm_p(s.opus.values, d, rho)
    rows.append(dict(compositor=k, n=len(s), rho=r, p=p2, p_unilateral=p1, periodo_ref=alvo_per, rho_dist=r2, p_dist=q2))
res = pd.DataFrame(rows)

# --- meta
w = np.sqrt(res.n.values); wmean = float((w * res.rho).sum() / w.sum())
npos = int((res.rho > 0).sum()); m = len(res)
sinal = binomtest(npos, m, 0.5, alternative="greater").pvalue
# nulo da média ponderada: permutar opus dentro de cada compositor
grp = [(s.opus.values, s.pc1.values) for _, s in sub[sub.composer_key.isin(res.compositor)].groupby("composer_key")]
ws = np.sqrt([len(g[0]) for g in grp])
nul = np.array([(ws * np.array([rho(rng.permutation(a), b) for a, b in grp])).sum() / ws.sum() for _ in range(NPERM)])
p_w = float((1 + np.sum(nul >= wmean)) / (NPERM + 1))
meta_res = dict(n_compositores=m, n_rho_positivo=npos, p_sinal_unilateral=float(sinal), media_ponderada_sqrt_n=wmean, p_media_perm_unilateral=p_w,
                var_pc1=expl, nperm=NPERM)
res.to_csv(HERE / "resultados_compositores.csv", index=False)
sub[["composer_key", "title", "opus", "pc1"]].sort_values(["composer_key", "opus"]).to_csv(HERE / "pecas_opus.csv", index=False)
(HERE / "metrics.json").write_text(json.dumps(dict(meta=meta_res, compositores=res.to_dict("records")), ensure_ascii=False, indent=1))
print(res.round(3).to_string()); print(meta_res)

# --- figura
conc = f"O opus quase não prevê o PC1 dentro da carreira: {npos} de {m} compositores com ρ > 0, média ponderada {wmean:.2f}; Scriabin e Beethoven ≈ 0" if p_w >= 0.05 else \
       f"Quanto maior o opus, mais 'recente' a peça: {npos} de {m} compositores com ρ > 0 (média ponderada {wmean:.2f})"
cols = 4; rws = int(np.ceil(m / cols))
fig, axs = plt.subplots(rws, cols, figsize=(13, 3.1 * rws), constrained_layout=True)
for ax in axs.ravel(): ax.set_visible(False)
for ax, (_, r) in zip(axs.ravel(), res.iterrows()):
    ax.set_visible(True); s = sub[sub.composer_key == r.compositor]
    dest = r.compositor.split(",")[0] in ("Scriabin", "Beethoven")
    c = "#b4421a" if dest else "#46607a"
    ax.scatter(s.opus, s.pc1, s=16, color=c, alpha=.8)
    b = np.polyfit(s.opus, s.pc1, 1); xx = np.array([s.opus.min(), s.opus.max()])
    ax.plot(xx, np.polyval(b, xx), color=c, lw=2 if dest else 1.2)
    ax.set_title(f"{r.compositor.split(',')[0]} (n={r.n}), ρ={r.rho:.2f}, p={r.p:.3f}", fontsize=9, fontweight="bold" if dest else "normal", color=c)
    ax.set_xlabel("opus", fontsize=8); ax.set_ylabel("PC1", fontsize=8); ax.tick_params(labelsize=7)
    if dest:
        for sp in ax.spines.values(): sp.set_color(c); sp.set_linewidth(1.8)
fig.suptitle(conc, fontsize=12, fontweight="bold")
fig.savefig(HERE / "figs" / "carreira.png", dpi=130)
