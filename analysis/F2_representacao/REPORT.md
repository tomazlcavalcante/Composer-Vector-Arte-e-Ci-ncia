# F2 — Escolha da representação

## Pergunta
Em que camada e com que pooling o modelo separa melhor, e de forma mais estável, a identidade do compositor?

## Hipótese registrada
"Camadas intermediárias ≥ última." (Está em `F2_representacao/README.md`, escrita como "≥ camada 6"; a seção 5 do PLANO.md não tem hipótese para a F2.)

## Configuração
- Só rótulo de compositor. Período e nacionalidade não são lidos.
- 2.183 peças, 52 compositores, 1 janela por peça (a do meio).
- Camadas 0 a 12, dois poolings (média da janela, último token). A grade do README era {2, 4, 6}; o `run.py` varreu as 13.
- Espaço centrado, norma 1 (cosseno).
- Critérios: acurácia balanceada (regressão logística, 5 dobras estratificadas; cada peça é uma unidade), pureza de 5 vizinhos, razão entre/intra, estabilidade (correlação entre distâncias de centróides de duas metades das peças, 10 repetições).
- Escolha: maior soma de acurácia balanceada e estabilidade.

## Resultado
| | camada | acurácia balanceada | pureza 5-NN | entre/intra | estabilidade |
|---|---|---|---|---|---|
| **Escolhida: média** | 6 | 0,301 | 0,277 | 0,316 | 0,791 |
| média | 5 | 0,297 | 0,272 | 0,302 | 0,795 |
| média | 12 (última) | 0,190 | 0,176 | 0,273 | 0,777 |
| último token (melhor) | 5 | 0,169 | 0,143 | 0,112 | 0,572 |
| último token | 12 (última) | 0,065 | 0,079 | 0,129 | 0,613 |

- Média, camadas 5 a 9: acurácia entre 0,291 e 0,301.
- Último token: no máximo 0,169, na camada 5.

## Comparação com o nulo
- Acaso = 1/52 = 0,019. Todas as camadas com média ficam acima (mínimo 0,152, camada 0). O último token na camada 0 fica em 0,036.
- Não há nulo por permutação nem intervalo de confiança nesta frente. Cada número é uma única execução da validação cruzada.

## O que não se pode concluir
- A hipótese se confirma na direção: no pooling média, 0,301 (camada 6) contra 0,190 (camada 12); no último token, 0,169 (camada 5) contra 0,065 (camada 12).
- Não dá para dizer que a camada 6 é melhor que a 5, 7, 8 ou 9. As diferenças são de 0,002 a 0,01, sem intervalo. A soma de critérios da 6 (1,092) e da 5 (1,091) é praticamente igual. Por isso o DIARIO guarda a 5 como secundária.
- Acurácia de 0,30 em 52 classes é bem acima do acaso, mas é baixa em termos absolutos. A identidade do compositor está só em parte nesse espaço (ver F4).
- A comparação média × último token mistura duas coisas: o pooling e o fato de a média ter a janela inteira. Não separa "o que o modelo sabe" de "quanto contexto o vetor resume".
- A camada foi escolhida e avaliada nos mesmos dados (otimismo pequeno, não medido).
- A camada 12 ruim pode ser efeito da especialização do modelo em prever o próximo token. Isso é interpretação, não foi testado.

## Figuras
- [Acurácia por camada](figs/camadas.png)

## Ideias fora do escopo
- Intervalo bootstrap por peças para a acurácia de cada camada.
- Nulo por permutação de rótulos.
- Branqueamento e métrica euclidiana (já previstos no PLANO como "fica para depois").
- Repetir com as janelas das passadas 2 e 3.
