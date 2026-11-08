# Exemplos de MIDI (F7, deslocamento)

Peça de origem: Bach, Sinfonia in G major, BWV 796 (primeira semente sorteada por `run.py` com `random_state=1`; ver `peca.txt`).
Gerado por `../exemplos_midi.py` (camada 6, vetor centrado de Chopin, norma = mediana de ‖h‖, top-p 0,98, `torch.manual_seed(0)` antes de cada condição).

| arquivo | conteúdo | notas | duração |
|---|---|---|---|
| `semente.mid` | só a semente: 50 notas (150 tokens) da peça de Bach | 50 | 4,4 s |
| `sem_steering.mid` | semente + 80 notas geradas sem steering | 130 | 10,2 s |
| `chopin_alfa1.mid` | semente + 80 notas com vetor de Chopin, α = 1 | 130 | 32,3 s |
| `chopin_alfa1_5.mid` | semente + 80 notas com vetor de Chopin, α = 1,5 | 130 | 23,8 s |

Nos três arquivos de continuação a semente é idêntica e está no início.

## Avisos
- É ilustração com uma única semente e uma única amostra por condição, não evidência. A evidência (7 sementes, controle aleatório, testes) está em `../REPORT.md`.
- Não há garantia de que o efeito do vetor seja audível nesta amostra; as durações diferem bastante entre as condições (andamento mais lento com steering aqui), o que pode ser acaso de uma amostra.
- O modelo gera só tempo, duração e altura (e instrumento): não há dinâmica (todas as notas com a mesma intensidade) nem pedal.
