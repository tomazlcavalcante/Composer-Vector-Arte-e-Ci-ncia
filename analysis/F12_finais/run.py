"""F12 / C2: finais de obra (Meyer). H13: a janela final (w3, 5/6) fica mais perto do centróide do
período/compositor que a inicial (w2, 1/6). Camada 6, pooling mean. Centróides sem a própria peça."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import wilcoxon, binomtest  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, center, l2norm  # noqa: E402

(HERE / "figs").mkdir(exist_ok=True)
X, df = load(6, "mean", windows=(1, 2, 3))
Xc, _ = center(X)               # média de todas as janelas
Z = l2norm(Xc)
meta = load_meta().set_index("composer_key")
df["periodo"] = df.composer_key.map(meta.periodo)

# peças com as 3 janelas
cnt = df.groupby("piece_id").window.nunique()
full = cnt[cnt == 3].index
pieces = pd.DataFrame(dict(piece_id=full))
pm = df.drop_duplicates("piece_id").set_index("piece_id")
pieces["composer"] = pm.loc[full, "composer_key"].values
pieces["periodo"] = pm.loc[full, "periodo"].values
pieces["title"] = pm.loc[full, "title"].values

pid = df.piece_id.values
win = df.window.values
idx = {(p, w): i for i, (p, w) in enumerate(zip(pid, win))}
# vetor-soma e contagem de janelas por peça, para centróides "leave-one-out" (média das janelas das outras peças)
def group_sums(keycol):
    S, N = {}, {}
    for k, g in df[df.piece_id.isin(full)].groupby(keycol):
        S[k] = Z[g.index.values].sum(0)
        N[k] = len(g)
    return S, N
dfp = df[df.piece_id.isin(full)]
S_c, N_c = group_sums("composer_key")
S_p, N_p = group_sums("periodo")

def cd(v, c):
    return 1 - float(v @ c) / (np.linalg.norm(v) * np.linalg.norm(c) + 1e-12)

rec = []
for _, r in pieces.iterrows():
    ii = {w: idx[(r.piece_id, w)] for w in (1, 2, 3)}
    own = sum(Z[i] for i in ii.values())
    row = dict(piece_id=r.piece_id, composer=r.composer, periodo=r.periodo)
    for name, S, N, key in (("comp", S_c, N_c, r.composer), ("per", S_p, N_p, r.periodo)):
        if N[key] - 3 < 3:  # sem outras peças
            for w in (1, 2, 3):
                row[f"{name}_w{w}"] = np.nan
            continue
        c = S[key] - own
        for w in (1, 2, 3):
            row[f"{name}_w{w}"] = cd(Z[ii[w]], c)
    row["d_start_end"] = cd(Z[ii[2]], Z[ii[3]])
    row["d_start_mid"] = cd(Z[ii[2]], Z[ii[1]])
    row["d_mid_end"] = cd(Z[ii[1]], Z[ii[3]])
    row["loss_start"] = df.loss.values[ii[2]]
    row["loss_mid"] = df.loss.values[ii[1]]
    row["loss_end"] = df.loss.values[ii[3]]
    rec.append(row)
R = pd.DataFrame(rec)
R["diff_comp"] = R.comp_w3 - R.comp_w2  # < 0: final mais perto
R["diff_per"] = R.per_w3 - R.per_w2
R.to_csv(HERE / "pecas.csv", index=False)


def tests(sub, col):
    s = sub[col].dropna()
    if len(s) < 6:
        return dict(n=int(len(s)))
    out = dict(n=int(len(s)), mean_diff=float(s.mean()), median_diff=float(s.median()),
               frac_final_closer=float((s < 0).mean()),
               wilcoxon_p_two=float(wilcoxon(s).pvalue), wilcoxon_p_less=float(wilcoxon(s, alternative="less").pvalue))
    cm = sub.dropna(subset=[col]).groupby("composer")[col].mean()
    cm = cm[cm != 0]
    k = int((cm < 0).sum())
    out.update(n_composers=int(len(cm)), composers_final_closer=k,
               sign_p_two=float(binomtest(k, len(cm), 0.5).pvalue),
               sign_p_less=float(binomtest(k, len(cm), 0.5, alternative="greater").pvalue))
    return out

m = dict(n_pieces_3w=int(len(R)), layer=6, pooling="mean")
for col in ("diff_comp", "diff_per"):
    m[col] = {"todos": tests(R, col)}
    for per, sub in R.groupby("periodo"):
        m[col][per] = tests(sub, col)
for c in ("comp", "per"):
    m[f"dist_media_{c}"] = {f"w{w}": float(R[f"{c}_w{w}"].mean()) for w in (1, 2, 3)}

# banalidades: distância início<->final e perda por posição
m["dist_intra"] = dict(start_end=float(R.d_start_end.mean()), start_mid=float(R.d_start_mid.mean()),
                       mid_end=float(R.d_mid_end.mean()),
                       wilcoxon_mid_end_vs_start_mid_p=float(wilcoxon(R.d_mid_end, R.d_start_mid).pvalue))
m["loss"] = dict(start=float(R.loss_start.mean()), mid=float(R.loss_mid.mean()), end=float(R.loss_end.mean()),
                 frac_end_lower_than_start=float((R.loss_end < R.loss_start).mean()),
                 wilcoxon_end_vs_start_p=float(wilcoxon(R.loss_end, R.loss_start).pvalue),
                 mean_diff_end_minus_start=float((R.loss_end - R.loss_start).mean()))
# a diferença de distância ao centróide se associa à perda? (pista de confusão)
from scipy.stats import spearmanr  # noqa: E402
ok = R.dropna(subset=["diff_per"])
m["spearman_diffper_vs_lossdiff"] = float(spearmanr(ok.diff_per, ok.loss_end - ok.loss_start).statistic)
# distâncias ao centróide: início vs meio vs final por período
m["por_periodo_media"] = {per: {f"per_w{w}": float(g[f"per_w{w}"].mean()) for w in (1, 2, 3)} for per, g in R.groupby("periodo")}
(HERE / "metrics.json").write_text(json.dumps(m, indent=1, ensure_ascii=False))

# --- figura ---
fig, ax = plt.subplots(1, 3, figsize=(14, 4.5))
for a, col, tt in ((ax[0], "diff_per", "Final - início: distância ao centróide do período"),
                   (ax[1], "diff_comp", "Final - início: distância ao centróide do compositor")):
    s = R[col].dropna()
    a.hist(s, bins=60, color="#1f77b4", alpha=.8)
    a.axvline(0, color="k", lw=1); a.axvline(s.mean(), color="r", ls="--", label=f"média {s.mean():+.4f}")
    a.set_title(tt, fontsize=9); a.set_xlabel("< 0: final mais perto"); a.legend()
pos = ["início (w2)", "meio (w1)", "final (w3)"]
ax[2].bar(pos, [R.loss_start.mean(), R.loss_mid.mean(), R.loss_end.mean()], color="#ff7f0e")
lo = min(R.loss_start.mean(), R.loss_mid.mean(), R.loss_end.mean())
ax[2].set_ylim(lo * 0.9, None)
ax[2].set_title("Perda média do modelo por posição", fontsize=9); ax[2].set_ylabel("loss (eixo truncado)")
fig.tight_layout(); fig.savefig(HERE / "figs" / "finais.png", dpi=140)
print(json.dumps(m, indent=1, ensure_ascii=False))
