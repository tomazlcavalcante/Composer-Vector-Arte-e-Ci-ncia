# Diário de decisões

## 2026-11-07, 20:50 — mudança de cenário

- Sem acesso à máquina do laboratório. O trabalho passa a rodar no ambiente do Claude: **2 núcleos de CPU, 7 GB de RAM, sem GPU**.
- Rede do ambiente: só GitHub e PyPI. Hugging Face, Google Drive e Zenodo estão **bloqueados**. Do GiantMIDI, só há aqui os 4 MIDIs de amostra do repositório oficial.
- Proposta do Thiago: usar um modelo pré-treinado da internet e, depois, o modelo dele.

### Ordem de decisão para o modelo

1. **Modelo do Thiago**, se o `state_dict` em fp16 (~40 MB) aparecer no repositório. Tem 20M de parâmetros e roda em CPU.
2. **Modelo pré-treinado do Hugging Face**, se o domínio for liberado. Preferência: Anticipatory Music Transformer small (stanford-crfm/music-small-800k, GPT-2, ~128M parâmetros, nativo em MIDI, treinado no Lakh MIDI). Ele não viu o GiantMIDI, o que deixa a análise fora da amostra de treino.
3. **Plano C**: corpus do music21 (via pip, com rótulo de compositor e época) e descritores simbólicos, sem transformer. Responde às perguntas Q1–Q3 com um espaço de estilo explícito; a Q4 fica só geométrica.

### Dados

GiantMIDI (subconjunto com sobrenome verificado). Precisa chegar ao ambiente por GitHub (o Tomaz envia os MIDIs) ou por liberação do Google Drive.

### Orçamento de CPU

Amostra de compositores com ≥ 20 peças (sem os contemporâneos de YouTube) e até 3 janelas por peça. Comandos de até 10 minutos, com resultados salvos incrementalmente.

## 2026-11-07, 21:20 — dados e modelo no ambiente

- **Domínios liberados** (huggingface.co, Google Drive). O zip do GiantMIDI veio do notebook do Tomaz pelo app. O subconjunto `surname_checked_midis` v1.2 (7.236 MIDIs) está em `/home/claude/data/giant/surname_checked_midis`.
- **Modelo:** Anticipatory Music Transformer small (`stanford-crfm/music-small-800k`): GPT-2 com 12 camadas, d = 768, contexto de 1.024 tokens, treinado no Lakh MIDI. O código do tokenizador (`jthickstun/anticipation`) foi instalado a partir do GitHub.
- **Sanidade:** perda de 2,88 num noturno de Chopin; cerca de 2 s por janela em CPU (2 núcleos).
- **Decisão sobre a entrada:** usar o formato do treino do AMT no modo autoregressivo, `[AUTOREGRESS]` seguido de 341 eventos (tempo, duração, nota), com tempo relativo ao início da janela e no máximo 100 s. Assim o modelo vê dados no formato em que foi treinado.
- **Decisão sobre a amostra:** 51 compositores com ≥ 20 peças (5 excluídos: contemporâneos de YouTube ou identidade incerta; ver `metadata_curated.csv`), 2.184 peças. Passada 1 = janela do meio de cada peça (cerca de 75 min); passadas 2 e 3 = janelas a 1/6 e 5/6, só se houver tempo. Mais Tico-Tico (Abreu) como ilustração.
- **Decisão sobre camadas:** salvar todas as 13 (embedding + 12 blocos), com último token e média. A F2 escolhe entre elas.
- **Metadados:** curados com conhecimento geral e marcados "verificar". Corrigidos os erros do GiantMIDI (Bach, Handel, Satie, Fauré, Brahms, Poulenc estavam como "British"). Período pela regra mecânica: nascimento + 30, cortes em 1600 / 1750 / 1820 / 1900, com a coluna `fronteira`.
- **Comando para retomar:** `python3 analysis/F0_infra/extract_amt.py --pass 1 --budget-min 9`. O script é retomável e pula o que já foi feito.

## 2026-11-07, ~23:30 — passada 1 concluída e primeiras análises

Base: 2.183 peças, 52 compositores, 1 janela (o meio) por peça.

- **F2 (representação):** a média sobre a janela supera o último token em todas as camadas. As camadas intermediárias são as melhores. **Escolhida: camada 6 com média.** Acurácia balanceada de 0,30 (acaso = 0,019), estabilidade dos centróides de 0,79. Secundária: camada 5. O último token, usado no artigo e no repositório original, tem no máximo 0,17. A hipótese da F2 (meio ≥ fim) se confirma; a camada 12, a última, é das piores (0,19).
- **F3 (mapa, H1/H2):** H1 confirmada. Mantel ρ = 0,48 (p < 0,001) entre a distância dos centróides e a diferença de ano de nascimento. H2: a nacionalidade tem ρ = 0,08 (p = 0,02) e some ao controlar a época (ρ = 0,04, p = 0,11). O PC1 do mapa segue a cronologia; o PC2 separa a música de dança sincopada (ragtime, Nazareth, Tico-Tico). Distorção da PCA: ρ de Spearman = 0,72.
  - Vizinhos mais próximos com sentido musical: Haydn ↔ Mozart, Bach ↔ Handel, Debussy ↔ Cyril Scott, Satie ↔ Rebikov, Medtner ↔ Schumann, Chopin → Scriabin, James Scott ↔ C. L. Johnson ↔ Joplin.
  - Tico-Tico: vizinhos C. L. Johnson, James Scott e Nazareth.
  - Ressalva: a lista de "afinidades inesperadas" por resíduo linear fica dominada por Victoria (300 anos de distância). Para o ensaio, usar a lista de vizinhos.
- **F4 (nuvens, H3/H4):** H3 confirmada. O compositor explica 23% da variância entre peças (nulo: 2,4%), e 69% das peças ficam mais perto do centróide de outro compositor: o estilo é mais nuvem que ponto. H4 **não** se confirma: o compositor pesa mais que o gênero (R² de 0,27 contra 0,13 nas mesmas peças). Mais compactos: Victoria e os ragtimes. Mais espalhados: Schubert, Schumann, Tchaikovsky, Busoni, Heller.
- **F5 (forma, H5):** não há lacuna maior que a de um nulo gaussiano sem grupos (razão 1,60, contra p95 do nulo de 2,27): o espaço é um **contínuo**. Mas a divisão em 2 grupos é estável (ARI = 0,79) e separa exatamente {Bach, Handel, Scarlatti, Haydn, Mozart, Beethoven, Hummel} de todo o resto. É um ramo "pré-romântico" (Barroco + Clássico), não só barroco.
- **F7a (caminho geométrico):** os compositores mais próximos do segmento Bach → Chopin incluem Beethoven (t = 0,39) e vários românticos com t entre 0,76 e 0,92. Dentro do segmento, t correlaciona com o ano de nascimento (ρ = 0,53).
- **F7b (steering, H6/H7):** vetor somado na camada 6, com norma igual à mediana de ‖h‖, α = 1, 7 sementes de Bach × 2 amostras, continuações de 120 tokens relidas sem steering. Progresso em direção a Chopin: nenhum 0,39; aleatório 0,43; centrado 0,68. Centrado > aleatório em 7 de 7 sementes (Wilcoxon p = 0,016). **H6 confirmada.** Caminho: t = 0 → 0,28; t = 0,5 → 0,34; t = 1 → 0,69. Monótono (H7), mas não linear: o ponto médio do vetor fica perto de Bach. Repetição de trigramas baixa em todas as condições (≤ 4%).
- **F6 (controles):** transpor ±2 ou ±5 semitons desloca a peça em 0,02–0,03, contra 0,54 de distância média da peça ao próprio centróide e 0,94 entre centróides. O "estilo" medido **não é tonalidade**; só 12% das peças trocam de centróide mais próximo. O número de peças não correlaciona com a distância bruta à média (ρ = −0,11) nem com a dispersão (ρ ≈ 0); o z de originalidade cresce com n por construção, então o ensaio deve usar a distância bruta.
- **Metadados:** a verificação web por subagente foi bloqueada (Wikipedia e IMSLP fora da lista de domínios); só Hitz foi confirmado. `fronteira` recalculada pela regra mecânica. Os valores seguem como "conhecimento geral (verificar)".

Próximos passos: passada 2 (janela a 1/6) para medir a variação dentro da obra (o estilo interno de Meyer) e reforçar a média por peça; REPORTs por frente; figuras para a apresentação; revisão independente.
