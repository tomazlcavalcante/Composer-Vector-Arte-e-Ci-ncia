# Composer Vector — um estudo sobre compositores e seus estilos

Ensaio para a disciplina **Artes e Ciência** (IMPA Tech), de Lucas Barbosa, Thiago Vinicius e Tomaz L. Cavalcante.

O trabalho analisa **como um Music Transformer organiza os compositores no seu espaço interno**. O modelo foi treinado no GiantMIDI-Piano, e o estilo de cada compositor é definido como a média das representações das suas obras ("composer vector", Jiang et al., 2026). Essa organização é confrontada com a noção de estilo de Leonard B. Meyer (1989). Não julgamos a qualidade das músicas geradas.

- Plano completo e versão de dois dias: [`PLANO.md`](PLANO.md) (o documento vivo do grupo está no Claude Docs).
- Código original do modelo: [thicius/composer-vector-ml2](https://github.com/thicius/composer-vector-ml2). O notebook usado no treino está em `referencia/`.

## Perguntas

| | Pergunta |
|---|---|
| Q1 | **Mapa:** quem fica perto de quem? A proximidade acompanha período e nacionalidade? |
| Q2 | **Ponto vs. nuvem:** quanto da variação entre peças é explicado pelo compositor? |
| Q3 | **Forma:** o espaço tem grupos separados ou é um contínuo? |
| Q4 | **Deslocamento:** somar o vetor de um compositor move a música na direção esperada? O que há entre Bach e Chopin? |

## Estrutura

```
analysis/
  common/            # modelo, leitura do acervo, extração e steering (somente leitura para F2–F7)
  data/              # tokenizer_config.json, training_history.json, metadados curados
  F0_infra/          # checkpoint, sanidade, extração das representações
  F1_metadados/      # seleção de compositores, nascimento, nacionalidade, período, gênero
  F2_representacao/  # escolha de camada, pooling e métrica (sem olhar para a história)
  F3_geometria/      # distâncias, Mantel, mapa (Q1)
  F4_nuvens/         # variância, dispersão, obras atípicas (Q2)
  F5_topologia/      # homologia persistente, Mapper (Q3)
  F6_controles/      # tamanho amostral, transposição, linha de base
  F7_deslocamento/   # steering e caminho Bach → Chopin (Q4)
referencia/          # notebook original do treino
```

Cada frente entrega `run.py`, `config.yaml`, `metrics.json`, `figs/` e um `REPORT.md` no modelo descrito em `PLANO.md`.

## Arquivos que não vão para o git

Ficam só na máquina do laboratório: checkpoint (`checkpoint_epoch_93.pt`), `composer_vectors.pt`, a pasta `surname_checked_midis/` e as representações extraídas (`analysis/data/embeddings/`). Os caminhos são configurados por variáveis de ambiente:

```bash
export CV_CHECKPOINT=/caminho/checkpoint_epoch_93.pt
export CV_MIDIS=/caminho/surname_checked_midis
export CV_EMBEDDINGS=/caminho/embeddings
```

## Ambiente

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

As versões de `miditok`, `symusic` e `tokenizers` estão fixadas porque são as gravadas no tokenizador do treino. Outra versão pode tokenizar diferente e invalidar o modelo. **Nunca retreine o tokenizador**: use sempre `analysis/data/tokenizer_config.json`.

## Referências

- Carlsson, G. Topology and data. *Bull. AMS* 46(2), 2009.
- Jiang, X. et al. Composer Vector: Style-steering Symbolic Music Generation in a Latent Space. arXiv:2604.03333, 2026.
- Kong, Q. et al. GiantMIDI-Piano. *TISMIR* 5(1), 2022.
- Meyer, L. B. *Style and Music: Theory, History, and Ideology*. 1989.
