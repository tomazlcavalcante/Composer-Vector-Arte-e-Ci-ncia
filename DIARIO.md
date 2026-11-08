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
