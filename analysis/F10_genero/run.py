"""F10 (B1): é época ou é gênero? Gênero da peça (GEN de F4, título) regredido para fora das representações.
Base: camada 6, média, janelas 1 e 2. Saídas: metrics.json, REPORT.md (escrito à mão a partir do metrics.json).
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

rng = np.random.default_rng(0)
X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Z0 = l2norm(center(Xp)[0])
y = dp.composer_key.values

GEN = {"sonata": r"sonat", "estudo": r"[ée]tude|study|studie", "valsa": r"valse|waltz|walzer", "mazurca": r"mazur",
       "noturno": r"noct", "prelúdio": r"pr[ée]lud", "fuga": r"fug", "rag": r"\brag", "variações": r"variat",
       "dança/minueto": r"menuet|minuet|dance|danse|tanz|polonaise|polka|gavotte|gigue",
       "romance/canção": r"romance|lied|song|chanson", "rapsódia": r"rhaps", "improviso": r"impromptu",
       "suíte": r"suite", "tango/choro": r"tango|choro|maxixe", "marcha": r"march|marche"}
gen = np.array([next((g for g, pat in GEN.items() if re.search(pat, t, re.I)), "outro") for t in dp.title])
cats = list(GEN) + ["outro"]
# one-hot com "outro" como referência + intercepto (equivale a one-hot completo com intercepto)
A = np.column_stack([np.ones(len(gen))] + [(gen == g).astype(float) for g in cats[:-1]])
beta, *_ = np.linalg.lstsq(A, Z0, rcond=None)
Zres = l2norm(Z0 - A @ beta)
frac_var_genero = float(1 - np.sum((Z0 - A @ beta) ** 2) / np.sum((Z0 - Z0.mean(0)) ** 2))

meta = load_meta().set_index("composer_key")
keys0 = sorted(set(y))
assert all(meta.loc[k, "incluir"] == 1 for k in keys0)
birth = meta.loc[keys0, "birth"].values.astype(float)
dyear = np.abs(birth[:, None] - birth[None])
iu = np.triu_indices(len(keys0), 1)
SUR = [k.split(",")[0] for k in keys0]
SHORT = [(k.split(",")[1].strip()[0] + ". " + s) if SUR.count(s) > 1 else s for k, s in zip(keys0, SUR)]


def r2(Z, y):
    tot = np.sum((Z - Z.mean(0)) ** 2)
    btw = sum((y == k).sum() * np.sum((Z[y == k].mean(0) - Z.mean(0)) ** 2) for k in set(y))
    return float(btw / tot)


def mantel(D, n_perm=5000, seed=1):
    r = np.random.default_rng(seed)
    r0 = spearmanr(D[iu], dyear[iu]).statistic
    cnt = sum(spearmanr(D[iu], dyear[np.ix_(p, p)][iu]).statistic >= r0
              for p in (r.permutation(len(keys0)) for _ in range(n_perm)))
    return float(r0), float((cnt + 1) / (n_perm + 1))


def analyse(Z):
    C, keys = centroids(Z, dp)
    assert keys == keys0
    D = cosine_dist(C)
    np.fill_diagonal(D, 0)
    D = np.clip((D + D.T) / 2, 0, None)
    rho, p = mantel(D)
    L = linkage(squareform(D, checks=False), "average")
    g = fcluster(L, 2, "maxclust")
    grp = {int(k): [SHORT[i] for i in np.where(g == k)[0]] for k in set(g)}
    bach = g[keys.index("Bach, Johann Sebastian")] if "Bach, Johann Sebastian" in keys else None
    return dict(mantel_rho=round(rho, 4), mantel_p=p, R2_compositor=round(r2(Z, y), 4), k2=grp), D, g


base, Db, gb = analyse(Z0)
ctrl, Dc, gc = analyse(Zres)
PRE = ["Bach", "Handel", "Scarlatti", "Haydn", "Mozart", "Beethoven", "Hummel"]
def blk(res):
    for v in res["k2"].values():
        if "Bach" in v:
            return sorted(v)
base["bloco_com_Bach"] = blk(base); ctrl["bloco_com_Bach"] = blk(ctrl)
for r in (base, ctrl):
    r["bloco_pre_romantico_contido"] = all(n in r["bloco_com_Bach"] for n in PRE)
    r["extras_alem_do_bloco_esperado"] = sorted(set(r["bloco_com_Bach"]) - set(PRE))
    r["tamanhos_k2"] = sorted(len(v) for v in r["k2"].values())
rsa = float(spearmanr(Db[iu], Dc[iu]).statistic)
n_by_gen = {g: int((gen == g).sum()) for g in cats}
out = dict(config=dict(layer=6, pooling="mean", windows=[1, 2], n_pieces=int(len(dp)), n_composers=len(keys0)),
           n_pecas_por_genero=n_by_gen, frac_variancia_explicada_pelo_genero=round(frac_var_genero, 4),
           sem_controle=base, residuos_de_genero=ctrl,
           spearman_distancias_base_vs_residuos=round(rsa, 4),
           H12=dict(cronologia_sobrevive=bool(ctrl["mantel_rho"] > 0.3), bloco_continua=bool(ctrl["bloco_pre_romantico_contido"])))
(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
