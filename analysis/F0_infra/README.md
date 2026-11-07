# F0 — Infraestrutura (bloqueante)

**Pergunta:** o checkpoint reproduz o treino, e que representações extraímos dele?

1. Carregar `$CV_CHECKPOINT` com `common.model.load_model` e o tokenizador `../data/tokenizer_config.json` (`REMI(params=...)`, nunca `train`).
2. Sanidade: perda média em ~500 fragmentos aleatórios ≈ 3,05 (log em `training_history.json`). Se não bater, parar e reportar.
3. Para todas as peças (`common.data.list_pieces`): tokenizar, fatiar com `common.data.fragments`, passar os 1023 primeiros tokens de cada fragmento por `hidden_states(layers=[2,4,6])` e gravar em `$CV_EMBEDDINGS` (float16): `last[layer]`, `mean[layer]`, `piece_id`, `composer_key`, `fragment_idx`, `loss`.
4. Tabela por peça: nº de tokens, nº de fragmentos, se foi descartada por ser curta.
5. Teste: centróide de 'Chopin, Frédéric' (camada 6, último token, média por fragmento) ≈ vetor salvo no `composer_vectors.pt` antigo.

**Saída:** arquivo de representações documentado, `pieces_tokens.csv`, `REPORT.md`.
