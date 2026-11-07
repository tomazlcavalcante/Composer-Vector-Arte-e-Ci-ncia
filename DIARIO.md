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
