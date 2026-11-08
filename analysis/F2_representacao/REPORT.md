# F2 — Escolha da representação

Base sem duplicatas (08/11): números atualizados; conclusões inalteradas.

## Pergunta
Em que camada e com que pooling o modelo separa melhor, e de forma mais estável, a identidade do compositor?

## Hipótese registrada
"Camadas intermediárias ≥ última." (Está em `F2_representacao/README.md`, escrita como "≥ camada 6"; a seção 5 do PLANO.md não tem hipótese para a F2.)

## Configuração
- Só rótulo de compositor. Período e nacionalidade não são lidos.
- 2.103 peças (depois de remover 80 cópias), 52 compositores. Cada peça é a média de 2 janelas (a do meio e a de 1/6); números finais do ensaio (passada 2). A passada 1 (1 janela) está em `metrics_passada1.json`.
- Camadas 0 a 12, dois poolings (média da janela, último token). A grade do README era {2, 4, 6}; o `run.py` varreu as 13.
- Espaço centrado, norma 1 (cosseno).
- Critérios: acurácia balanceada (regressão logística, 5 dobras estratificadas; cada peça é uma unidade), pureza de 5 vizinhos, razão entre/intra, estabilidade (correlação entre distâncias de centróides de duas metades das peças, 10 repetições).
- Escolha: maior soma de acurácia balanceada e estabilidade.

## Resultado
| | camada | acurácia balanceada | pureza 5-NN | entre/intra | estabilidade |
|---|---|---|---|---|---|
| **Escolhida: média** | 6 | 0,311 | 0,305 | 0,394 | 0,829 |
| média | 5 | 0,308 | 0,295 | 0,378 | 0,811 |
| média | 12 (última) | 0,186 | 0,176 | 0,338 | 0,779 |
| último token (melhor) | 5 | 0,166 | 0,161 | 0,151 | 0,707 |
| último token | 12 (última) | 0,057 | 0,060 | 0,155 | 0,637 |

- Média, camadas 5 a 9: acurácia entre 0,299 e 0,311 (a camada 8 tem 0,3111, ligeiramente acima da 6, com 0,3106).
- Último token: no máximo 0,166, na camada 5.
- **Passada 1 (1 janela, base com cópias), para comparar:** camada 6 com média tinha acurácia balanceada de 0,301 e estabilidade de 0,791; com 2 janelas e sem cópias, 0,311 e 0,829. A escolha (camada 6, média) e a ordem média > último token não mudaram; a camada 12 continua entre as piores (0,190 → 0,186).
- **Decisão sobre a camada (base sem cópias).** As camadas 5 a 9 ficam empatadas: a soma acurácia + estabilidade é 1,118 (5), 1,139 (6), 1,150 (7), 1,137 (8) e 1,138 (9). O campo `melhor_pelo_criterio` do `metrics.json` mostra a **camada 7** (1,150). **Mantida a camada 6**, escolhida antes da descoberta das duplicatas. A regra, escrita no `run.py`, é manter a camada 6 se ela estiver a até 0,02 da melhor soma (aqui a diferença é de 0,010), o que evita reabrir a escolha depois de ver os dados. O campo `best` do `metrics.json` é a camada 6.

## Comparação com o nulo
- Acaso = 1/52 = 0,019. Todas as camadas com média ficam acima (mínimo 0,136, camada 0). O último token na camada 0 fica em 0,028.
- Não há nulo por permutação nem intervalo de confiança nesta frente. Cada número é uma única execução da validação cruzada.

## O que não se pode concluir
- A hipótese se confirma na direção: no pooling média, 0,311 (camada 6) contra 0,186 (camada 12); no último token, 0,166 (camada 5) contra 0,057 (camada 12).
- Não dá para dizer que a camada 6 é melhor que a 5, 7, 8 ou 9. As diferenças de acurácia da 6 para as camadas 5, 7, 8 e 9 vão de −0,0005 (a 8 é um pouco maior) a 0,011, sem intervalo. Pela soma de critérios, a 7 (1,150) fica 0,010 acima da 6 (1,139) e a 5 (1,118), 0,021 abaixo. O DIARIO guarda a 5 como secundária.
- Acurácia de 0,31 em 52 classes é bem acima do acaso, mas é baixa em termos absolutos. A identidade do compositor está só em parte nesse espaço (ver F4).
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
