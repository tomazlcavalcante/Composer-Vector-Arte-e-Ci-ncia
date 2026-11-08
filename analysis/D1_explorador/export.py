"""Exporta os dados do explorador interativo (mapa de compositores e peças) para dados.json."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, load_meta, piece_level, center, l2norm, centroids, cosine_dist

X, df = load(6, "mean", windows=(1, 2))
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp); Z = l2norm(Xc)
C, keys = centroids(Z, dp)
Cm = C.mean(0)
U, S, Vt = np.linalg.svd(C - Cm, full_matrices=False)
meta = load_meta().set_index("composer_key")
birth = meta.loc[keys, "birth"].values.astype(float)
if np.corrcoef((C - Cm) @ Vt[0], birth)[0, 1] < 0: Vt[0] *= -1
P = (C - Cm) @ Vt[:2].T
Pp = (Z - Cm) @ Vt[:2].T
D = cosine_dist(C)
expl = (S**2 / (S**2).sum())[:2]
sur = pd.read_csv(HERE.parent / "F8_expectativa" / "surpresa_por_compositor.csv")
scol = [c for c in sur.columns if "media" in c.lower() or "mean" in c.lower()][0]
kcol = [c for c in sur.columns if "compos" in c.lower()][0]
smap = dict(zip(sur[kcol], sur[scol]))
disp = pd.read_csv(HERE.parent / "F4_nuvens" / "dispersao.csv").set_index("composer").dispersao.to_dict()
sur_names = [k.split(",")[0] for k in keys]
short = [(k.split(",")[1].strip()[0] + ". " + s) if sur_names.count(s) > 1 else s for k, s in zip(keys, sur_names)]
comps = []
for i, k in enumerate(keys):
    nn = np.argsort(D[i])[1:4]
    m = meta.loc[k]
    comps.append(dict(key=k, nome=short[i], nasc=int(m.birth), morte=int(m.death) if not pd.isna(m.death) else None,
        nac=m.nationality, periodo=m.periodo, n=int((dp.composer_key == k).sum()), x=round(float(P[i,0]),4), y=round(float(P[i,1]),4),
        viz=[dict(i=int(j), d=round(float(D[i,j]),3)) for j in nn], surpresa=round(float(smap.get(k, np.nan)),3),
        dispersao=round(float(disp.get(k, np.nan)),3)))
idx = {k: i for i, k in enumerate(keys)}
pecas = [dict(c=idx[r.composer_key], t=r.title[:70], x=round(float(Pp[j,0]),3), y=round(float(Pp[j,1]),3)) for j, r in dp.iterrows()]
Xe, de = load(6, "mean", windows=(1, 2), include_extra=True)
tt = de.composer_key.str.startswith("Abreu").values
zt = l2norm(Xe[tt].mean(0, keepdims=True) - mu); pt = ((zt - Cm) @ Vt[:2].T)[0]
dt = cosine_dist(zt, C)[0]
out = dict(compositores=comps, pecas=pecas, tico=dict(x=round(float(pt[0]),4), y=round(float(pt[1]),4), viz=[dict(i=int(j), d=round(float(dt[j]),3)) for j in np.argsort(dt)[:3]]),
           pca_expl=[round(float(e),3) for e in expl], info=dict(modelo="Anticipatory Music Transformer small (Lakh MIDI)", camada=6, pooling="média", janelas=2,
           n_pecas=int(len(dp)), mantel=0.505, r2=0.275))
(HERE / "dados.json").write_text(json.dumps(out, ensure_ascii=False))
print(len(comps), len(pecas), round((HERE / "dados.json").stat().st_size/1024), "KB", expl)
