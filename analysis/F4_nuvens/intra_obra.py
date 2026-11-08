"""F4b: estilo interno da obra (nível "intra-opus" de Meyer).

Usa as peças com duas ou mais janelas (passadas 1 e 2: meio e 1/6 da peça). Compara três distâncias
cosseno (espaço centrado, camada/pooling da F2):
  - entre janelas da MESMA peça;
  - entre janelas de peças diferentes do MESMO compositor;
  - entre janelas de compositores DIFERENTES.
Se a variação dentro da obra for comparável à variação entre obras do mesmo compositor, a "nuvem"
do compositor já está, em parte, dentro de cada obra.
Também refaz R² e acurácia de centróide com a média de 2 janelas por peça, para checar se os números
da passada 1 se mantêm.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, piece_level, center, l2norm, cosine_dist  # noqa: E402

cfg = json.loads((HERE.parent / "F2_representacao" / "metrics.json").read_text())["best"]
LAYER, POOL = cfg["layer"], cfg["pooling"]
rng = np.random.default_rng(0)

X, df = load(LAYER, POOL, windows=(1, 2))
mu = X.mean(0)
Z = l2norm(X - mu)
multi = df.groupby("piece_id").window.transform("size") >= 2
Zm, dm = Z[multi.values], df[multi].reset_index(drop=True)
pid, comp = dm.piece_id.values, dm.composer_key.values

D = cosine_dist(Zm)
iu = np.triu_indices(len(dm), 1)
same_p = (pid[:, None] == pid[None])[iu]
same_c = (comp[:, None] == comp[None])[iu]
d = D[iu]
res = dict(n_pecas_com_2_janelas=int(dm.piece_id.nunique()),
           dist_mesma_peca=round(float(d[same_p].mean()), 4),
           dist_mesmo_compositor_outra_peca=round(float(d[same_c & ~same_p].mean()), 4),
           dist_compositores_diferentes=round(float(d[~same_c].mean()), 4))
# fração da variância entre janelas explicada por peça e por compositor
tot = np.sum((Zm - Zm.mean(0)) ** 2)


def btw(labels):
    return sum((labels == k).sum() * np.sum((Zm[labels == k].mean(0) - Zm.mean(0)) ** 2) for k in set(labels)) / tot


res["R2_janelas_por_peca"] = round(float(btw(pid)), 4)
res["R2_janelas_por_compositor"] = round(float(btw(comp)), 4)

# R² no nível de peça com 2 janelas (comparar com F4: 0,23 com 1 janela)
Xp, dp = piece_level(X[multi.values], df[multi].reset_index(drop=True))
Zp = l2norm(center(Xp)[0])
y = dp.composer_key.values
totp = np.sum((Zp - Zp.mean(0)) ** 2)
res["R2_compositor_nivel_peca_2janelas"] = round(float(sum((y == k).sum() * np.sum((Zp[y == k].mean(0) - Zp.mean(0)) ** 2)
                                                             for k in set(y)) / totp), 4)
(HERE / "metrics_intra_obra.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))

# --- robustez: por compositor, a distância média entre janelas da mesma peça é menor que entre peças? ---
per = []
for k in sorted(set(comp)):
    m = comp == k
    Dk = D[np.ix_(m, m)]
    pk = pid[m]
    iuk = np.triu_indices(m.sum(), 1)
    sp = (pk[:, None] == pk[None])[iuk]
    dk = Dk[iuk]
    per.append(dict(composer=k, mesma_peca=float(dk[sp].mean()), outra_peca=float(dk[~sp].mean())))
import pandas as pd  # noqa: E402
per = pd.DataFrame(per)
per.to_csv(HERE / "intra_obra_por_compositor.csv", index=False)
diff = (per.outra_peca - per.mesma_peca).values
boot = [rng.choice(diff, len(diff)).mean() for _ in range(2000)]
res["por_compositor_frac_mesma_peca_mais_perto"] = round(float((diff > 0).mean()), 3)
res["por_compositor_diferenca_media"] = round(float(diff.mean()), 4)
res["por_compositor_diferenca_ic95"] = [round(float(x), 4) for x in np.percentile(boot, [2.5, 97.5])]
(HERE / "metrics_intra_obra.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))
