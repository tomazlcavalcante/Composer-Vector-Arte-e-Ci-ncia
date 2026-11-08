"""F4: ponto contra nuvem (Q2, hipóteses H3 e H4).

- Fração da variância (nível de peça) explicada pelo compositor (R² de ANOVA multivariada = traço
  entre / traço total), comparada a um nulo de rótulos permutados.
- Dispersão por compositor com n igualado (subamostragem de 20 peças, 200 repetições).
- Sobreposição: fração das peças mais próximas do centróide de outro compositor (centróide próprio
  recalculado sem a peça).
- Gênero contra compositor (H4): distância entre peças do mesmo compositor e gêneros diferentes
  vs. mesmo gênero e compositores diferentes.
- Obras atípicas: peças mais distantes do próprio centróide.
"""
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

cfg = json.loads((HERE.parent / "F2_representacao" / "metrics.json").read_text())["best"]
LAYER, POOL = cfg["layer"], cfg["pooling"]
rng = np.random.default_rng(0)
(HERE / "figs").mkdir(exist_ok=True)

X, df = load(LAYER, POOL)
Xp, dp = piece_level(X, df)
Z = l2norm(center(Xp)[0])
y = dp.composer_key.values
keys = sorted(set(y))


def r2(Z, y):
    tot = np.sum((Z - Z.mean(0)) ** 2)
    btw = sum((y == k).sum() * np.sum((Z[y == k].mean(0) - Z.mean(0)) ** 2) for k in set(y))
    return btw / tot


R2 = r2(Z, y)
R2_null = [r2(Z, rng.permutation(y)) for _ in range(200)]

# dispersão com n igualado
N_EQ = 20
disp = {}
for k in keys:
    idx = np.where(y == k)[0]
    vals = []
    for _ in range(200):
        s = rng.choice(idx, N_EQ, replace=len(idx) < N_EQ)
        c = Z[s].mean(0)
        vals.append(np.mean(np.sum((Z[s] - c) ** 2, 1)))
    disp[k] = float(np.mean(vals))
meta = load_meta().set_index("composer_key")
disp_tab = pd.DataFrame(dict(composer=list(disp), dispersao=np.round(list(disp.values()), 4),
                             periodo=meta.loc[list(disp), "periodo"].values,
                             n_pecas=[int((y == k).sum()) for k in disp])).sort_values("dispersao")
disp_tab.to_csv(HERE / "dispersao.csv", index=False)

# sobreposição (deixando a peça de fora do próprio centróide)
C, ck = centroids(Z, dp)
sums = {k: Z[y == k].sum(0) for k in ck}
cnt = {k: (y == k).sum() for k in ck}
own_far, nearest_other = [], []
for i in range(len(y)):
    k = y[i]
    Cl = C.copy()
    j = ck.index(k)
    Cl[j] = (sums[k] - Z[i]) / (cnt[k] - 1)
    d = cosine_dist(Z[i:i + 1], Cl)[0]
    nearest_other.append(ck[int(np.argmin(d))])
    own_far.append(float(d[j]))
dp["dist_proprio"] = own_far
dp["centroide_mais_proximo"] = nearest_other
overlap = float(np.mean(dp.centroide_mais_proximo != dp.composer_key))
conf = dp.groupby("composer_key").apply(lambda g: (g.centroide_mais_proximo == g.name).mean()).rename("acerto")
conf.to_csv(HERE / "acerto_centroide.csv")

# obras atípicas: z-score da distância ao próprio centróide dentro do compositor
dp["z_atipico"] = dp.groupby("composer_key").dist_proprio.transform(lambda s: (s - s.mean()) / (s.std() + 1e-9))
dp.sort_values("z_atipico", ascending=False).head(40)[
    ["composer_key", "title", "dist_proprio", "z_atipico", "centroide_mais_proximo"]].to_csv(HERE / "obras_atipicas.csv", index=False)

# gênero por palavra-chave
GEN = {"sonata": r"sonat", "estudo": r"[ée]tude|study|studie", "valsa": r"valse|waltz|walzer", "mazurca": r"mazur",
       "noturno": r"noct", "prelúdio": r"pr[ée]lud", "fuga": r"fug", "rag": r"\brag", "variações": r"variat",
       "dança/minueto": r"menuet|minuet|dance|danse|tanz|polonaise|polka|gavotte|gigue",
       "romance/canção": r"romance|lied|song|chanson", "rapsódia": r"rhaps", "improviso": r"impromptu",
       "suíte": r"suite", "tango/choro": r"tango|choro|maxixe", "marcha": r"march|marche"}
dp["genero"] = [next((g for g, pat in GEN.items() if re.search(pat, t, re.I)), "outro") for t in dp.title]
mask = (dp.genero != "outro").values
Zg, yg, gg = Z[mask], y[mask], dp.genero.values[mask]
Dg = cosine_dist(Zg)
iu = np.triu_indices(len(yg), 1)
same_c = (yg[:, None] == yg[None])[iu]
same_g = (gg[:, None] == gg[None])[iu]
d = Dg[iu]
h4 = dict(mesmo_compositor_genero_diferente=float(d[same_c & ~same_g].mean()),
          mesmo_genero_compositor_diferente=float(d[~same_c & same_g].mean()),
          mesmo_compositor_mesmo_genero=float(d[same_c & same_g].mean()),
          tudo_diferente=float(d[~same_c & ~same_g].mean()),
          n_pecas_com_genero=int(mask.sum()))
h4["R2_genero"] = float(r2(Zg, gg))
h4["R2_compositor_mesmas_pecas"] = float(r2(Zg, yg))

fig, ax = plt.subplots(figsize=(7, 10))
cols = {"Renascimento": "#8c564b", "Barroco": "#d62728", "Clássico": "#ff7f0e", "Romântico": "#1f77b4", "Moderno": "#2ca02c"}
_sur = [c.split(",")[0] for c in disp_tab.composer]
labels = [(c.split(",")[1].strip()[0] + ". " + sn) if _sur.count(sn) > 1 else sn for c, sn in zip(disp_tab.composer, _sur)]
ax.barh(labels, disp_tab.dispersao, color=[cols.get(p, "gray") for p in disp_tab.periodo])
ax.set_xlabel(f"dispersão média intra-compositor (n = {N_EQ} peças por sorteio)")
ax.set_title("Quão espalhada é a obra de cada compositor")
fig.tight_layout()
fig.savefig(HERE / "figs" / "dispersao.png", dpi=150)

out = dict(layer=LAYER, pooling=POOL, H3_R2_compositor=round(float(R2), 4),
           H3_R2_nulo_media=round(float(np.mean(R2_null)), 4), H3_R2_nulo_p95=round(float(np.percentile(R2_null, 95)), 4),
           sobreposicao_frac_pecas_mais_perto_de_outro=round(overlap, 4), H4=h4,
           mais_compactos=disp_tab.composer.head(5).tolist(), mais_espalhados=disp_tab.composer.tail(5).tolist())
(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
