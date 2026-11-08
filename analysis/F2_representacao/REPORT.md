# F2 — Escolha da representação

## Pergunta
Em que camada e com que pooling o modelo separa melhor, e de forma mais estável, a identidade do compositor?

## Hipótese registrada
"Camadas intermediárias ≥ última." (Está em `F2_representacao/README.md`, escrita como "≥ camada 6"; a seção 5 do PLANO.md não tem hipótese para a F2.)

## Configuração
- Só rótulo de compositor. Período e nacionalidade não são lidos.
- 2.183 peças, 52 compositores. Cada peça é a média de 2 janelas (a do meio e a de 1/6); números finais do ensaio (passada 2). A passada 1 (1 janela) está em `metrics_passada1.json`.
- Camadas 0 a 12, dois poolings (média da janela, último token). A grade do README era {2, 4, 6}; o `run.py` varreu as 13.
- Espaço centrado, norma 1 (cosseno).
- Critérios: acurácia balanceada (regressão logística, 5 dobras estratificadas; cada peça é uma unidade), pureza de 5 vizinhos, razão entre/intra, estabilidade (correlação entre distâncias de centróides de duas metades das peças, 10 repetições).
- Escolha: maior soma de acurácia balanceada e estabilidade.

## Resultado
| | camada | acurácia balanceada | pureza 5-NN | entre/intra | estabilidade |
|---|---|---|---|---|---|
| **Escolhida: média** | 6 | 0,349 | 0,324 | 0,399 | 0,834 |
| média | 5 | 0,340 | 0,315 | 0,383 | 0,843 |
| média | 12 (última) | 0,211 | 0,203 | 0,351 | 0,814 |
| último token (melhor) | 5 | 0,203 | 0,188 | 0,154 | 0,707 |
| último token | 12 (última) | 0,084 | 0,088 | 0,162 | 0,641 |

- Média, camadas 5 a 9: acurácia entre 0,332 e 0,349.
- Último token: no máximo 0,203, na camada 5.
- **Passada 1 (1 janela), para comparar:** camada 6 com média tinha acurácia balanceada de 0,301 e estabilidade de 0,791; com 2 janelas, 0,349 e 0,834. A escolha (camada 6, média; camada 5 muito próxima) e a ordem média > último token não mudaram; a camada 12 continua entre as piores (0,190 → 0,211).

## Comparação com o nulo
- Acaso = 1/52 = 0,019. Todas as camadas com média ficam acima (mínimo 0,172, camada 0). O último token na camada 0 fica em 0,045.
- Não há nulo por permutação nem intervalo de confiança nesta frente. Cada número é uma única execução da validação cruzada.

## O que não se pode concluir
- A hipótese se confirma na direção: no pooling média, 0,349 (camada 6) contra 0,211 (camada 12); no último token, 0,203 (camada 5) contra 0,084 (camada 12).
- Não dá para dizer que a camada 6 é melhor que a 5, 7, 8 ou 9. As diferenças de acurácia da 6 para as camadas 5, 7, 8 e 9 vão de 0,007 a 0,017, sem intervalo. A soma de critérios da 6 (1,183) e da 5 (1,183) é praticamente igual (diferença de 0,0005). Por isso o DIARIO guarda a 5 como secundária.
- Acurácia de 0,35 em 52 classes é bem acima do acaso, mas é baixa em termos absolutos. A identidade do compositor está só em parte nesse espaço (ver F4).
- A comparação média × último token mistura duas coisas: o pooling e o fato de a média ter a janela inteira. Não separa "o que o modelo sabe" de "quanto contexto o vetor resume".
- A camada foi escolhida e avaliada nos mesmos dados (otimismo pequeno, não medido).
- A camada 12 ruim pode ser efeito da especialização do modelo em prever o próximo token. Isso é interpretação, não foi testado.

## Figuras
- [Acurácia por camada](figs/camadas.png)

## Ideias fora do escopo
- Intervalo bootstrap por peças para a acurácia de cada camada.
- Nulo por permutação de rótulos.
- Branqueamento e métrica euclidiana (já previstos no PLANO como "fica para depois").
- Repetir com a janela da passada 3 (5/6), se houver.
