"""F2: escolha de camada e pooling usando SÓ o rótulo de compositor.

Critérios (todos no nível de peça, espaço centrado):
  - acurácia balanceada de regressão logística, validação cruzada estratificada em 5 dobras
    (cada peça é uma unidade, então a divisão já é por peça);
  - pureza de 5 vizinhos (cosseno);
  - razão entre/intra: variância dos centróides / variância média dentro do compositor;
  - estabilidade: correlação entre matrizes de distância de centróides de duas metades aleatórias das peças.
Período e nacionalidade não são lidos aqui (princípio 1 do PLANO).
"""
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import balanced_accuracy_score
from sklearn.neighbors import NearestNeighbors
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from analysis.common.emb import load, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

rng = np.random.default_rng(0)
results = []
for pooling in ["mean", "last"]:
    for layer in range(13):
        X, df = load(layer, pooling)
        Xp, dp = piece_level(X, df)
        ok = dp.composer_key.map(dp.composer_key.value_counts()) >= 5  # só importa em execuções parciais
        Xp, dp = Xp[ok.values], dp[ok].reset_index(drop=True)
        Xc, _ = center(Xp)
        y = dp.composer_key.values
        Z = l2norm(Xc)
        clf = LogisticRegression(max_iter=2000, C=1.0)
        cv = StratifiedKFold(5, shuffle=True, random_state=0)
        pred = cross_val_predict(clf, Z, y, cv=cv)
        bacc = balanced_accuracy_score(y, pred)
        nn = NearestNeighbors(n_neighbors=6, metric="cosine").fit(Z)
        _, ind = nn.kneighbors(Z)
        purity = float(np.mean(y[ind[:, 1:]] == y[:, None]))
        C, keys = centroids(Z, dp)
        between = np.mean(np.sum((C - Z.mean(0)) ** 2, 1))
        within = np.mean([np.mean(np.sum((Z[y == k] - C[i]) ** 2, 1)) for i, k in enumerate(keys)])
        stab = []
        for _ in range(10):
            half = rng.random(len(y)) < 0.5
            C1, k1 = centroids(Z[half], dp[half].reset_index(drop=True))
            C2, k2 = centroids(Z[~half], dp[~half].reset_index(drop=True))
            common = sorted(set(k1) & set(k2))
            D1 = cosine_dist(C1[[k1.index(k) for k in common]])
            D2 = cosine_dist(C2[[k2.index(k) for k in common]])
            iu = np.triu_indices(len(common), 1)
            stab.append(spearmanr(D1[iu], D2[iu]).statistic)
        r = dict(pooling=pooling, layer=layer, n_pieces=len(y), n_composers=len(keys), bal_acc=round(bacc, 4),
                 knn_purity=round(purity, 4), between_within=round(float(between / within), 4),
                 stability=round(float(np.mean(stab)), 4))
        print(r, flush=True)
        results.append(r)

chance = 1 / results[0]["n_composers"]
best = max(results, key=lambda r: r["bal_acc"] + (0 if np.isnan(r["stability"]) else r["stability"]))
# critério: acurácia balanceada + estabilidade (ambos em [0, 1], mesmo peso)
(HERE / "metrics.json").write_text(json.dumps(dict(results=results, chance=chance, best=best), indent=1))
print("escolhida:", best)
