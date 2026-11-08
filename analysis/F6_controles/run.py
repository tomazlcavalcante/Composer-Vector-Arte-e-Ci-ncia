"""F6: controles da versão de dois dias.

1. Tamanho amostral: correlação (Spearman) entre nº de peças e (a) distância à média geral (F3),
   (b) dispersão (F4). Uma correlação forte indicaria que "originalidade" ou "variedade" são efeito de n.
2. Transposição: para uma amostra de peças, transpõe ±2 e ±5 semitons, re-extrai a janela do meio e mede
   (a) o deslocamento cosseno, comparado às distâncias entre centróides, e (b) se o centróide mais próximo muda.
   Se transpor desloca tanto quanto trocar de compositor, o "estilo" é em boa parte tonalidade/registro.
Uso: python run.py [--n 80] (a parte 2 leva ~2 s por peça e transposição)
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "F0_infra"))
from analysis.common.emb import load, piece_level, center, l2norm, centroids, cosine_dist  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=80)
args = ap.parse_args()
cfg = json.loads((HERE.parent / "F2_representacao" / "metrics.json").read_text())["best"]
LAYER, POOL = cfg["layer"], cfg["pooling"]
rng = np.random.default_rng(0)
out = dict(layer=LAYER, pooling=POOL)

# 1. tamanho amostral
f3 = pd.read_csv(HERE.parent / "F3_geometria" / "distancias_media_geral.csv")
f4 = pd.read_csv(HERE.parent / "F4_nuvens" / "dispersao.csv")
out["n_vs_dist_media_geral"] = round(float(spearmanr(f3.n_pecas, f3.dist_media_geral).statistic), 3)
out["n_vs_z_originalidade"] = round(float(spearmanr(f3.n_pecas, f3.z_originalidade).statistic), 3)
out["n_vs_dispersao"] = round(float(spearmanr(f4.n_pecas, f4.dispersao).statistic), 3)

# 2. transposição
import torch  # noqa: E402
from transformers import AutoModelForCausalLM  # noqa: E402
from anticipation.convert import midi_to_events  # noqa: E402
from anticipation.vocab import AUTOREGRESS, NOTE_OFFSET  # noqa: E402
from extract_amt import window  # noqa: E402
from analysis.common.data import list_pieces  # noqa: E402

X, df = load(LAYER, POOL)
Xp, dp = piece_level(X, df)
Xc, mu = center(Xp)
Z = l2norm(Xc)
C, keys = centroids(Z, dp)
Dc = cosine_dist(C)
iu = np.triu_indices(len(keys), 1)

model = AutoModelForCausalLM.from_pretrained("/home/claude/models/music-small-800k").eval()
paths = {p.piece_id: p.path for p in list_pieces("/home/claude/data/giant/surname_checked_midis")}
sample = dp.sample(min(args.n, len(dp)), random_state=0)


def embed(seq):
    x = torch.tensor([[AUTOREGRESS] + seq])
    with torch.no_grad():
        hs = model(x, output_hidden_states=True).hidden_states[LAYER][0]
    v = (hs[1:].mean(0) if POOL == "mean" else hs[-1]).numpy()
    return l2norm((v - mu)[None])[0]


def transpose(seq, k):
    s = list(seq)
    for i in range(2, len(s), 3):
        pitch = (s[i] - NOTE_OFFSET) % 128
        if not 0 <= pitch + k < 128:
            return None
        s[i] += k
    return s


rows = []
for _, r in sample.iterrows():
    seq = window(midi_to_events(str(paths[r.piece_id])), 0.5)
    if seq is None:
        continue
    z0 = embed(seq)
    near0 = keys[int(np.argmin(cosine_dist(z0[None], C)[0]))]
    for k in (-5, -2, 2, 5):
        st = transpose(seq, k)
        if st is None:
            continue
        zk = embed(st)
        near = keys[int(np.argmin(cosine_dist(zk[None], C)[0]))]
        rows.append(dict(piece_id=r.piece_id, composer=r.composer_key, semitons=k,
                         deslocamento=float(1 - z0 @ zk), muda_vizinho=near != near0))
tr = pd.DataFrame(rows)
tr.to_csv(HERE / "transposicao.csv", index=False)
# referência: distância de uma peça ao centróide do próprio compositor (variação natural)
own = np.array([1 - Z[i] @ l2norm(C[keys.index(dp.composer_key.values[i])][None])[0] for i in range(len(dp))])
out["transposicao"] = dict(
    n_pecas=int(tr.piece_id.nunique()),
    deslocamento_medio_por_semitons=tr.groupby(tr.semitons.abs()).deslocamento.mean().round(4).to_dict(),
    frac_muda_centroide_mais_proximo=round(float(tr.muda_vizinho.mean()), 3),
    ref_dist_media_entre_centroides=round(float(Dc[iu].mean()), 4),
    ref_dist_media_peca_ao_proprio_centroide=round(float(own.mean()), 4),
)
(HERE / "metrics.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
