# F7 — Deslocamento (Q4)

## Pergunta
Somar o vetor de um compositor move a música na direção esperada? O que há entre Bach e Chopin?

## Hipótese registrada
- **H6:** o vetor centrado desloca a música relida em direção ao alvo mais que um vetor aleatório e mais que a continuação sem steering, de forma monótona em α até a quebra.
- **H7:** no caminho Bach → Chopin a posição relida avança de forma monótona. Se os pontos intermediários caem perto dos clássicos é uma pergunta aberta.

## Configuração
- Camada 6, pooling média. Um único par: Bach → Chopin.
- **(a) Geométrico:** distância de cada outro centróide ao segmento Bach → Chopin e parâmetro t da projeção. Distância Bach–Chopin: 0,880.
- **(b) Steering:** vetor somado na camada 6 (forma h ← (h + αv)|h|/|h + αv|), norma igual à mediana de ‖h‖. 120 tokens novos a partir de 50 eventos de semente. Continuação relida sem steering.
- Progresso = projeção na direção Bach → Chopin (0 = centróide de Bach, 1 = centróide de Chopin).
- Condições: nenhum, aleatório (mesma norma), centrado (centróide de Chopin menos média geral) e caminho (1−t)·v_Bach + t·v_Chopin com t = 0, 0,5 e 1.
- **Principal: `steering_forte.csv`**, α = 1, 7 sementes de Bach × 2 amostras = 14 continuações por condição. Piloto: `steering_piloto.csv`, 3 sementes × 2 = 6 por condição.

## Resultado
**(a) Caminho geométrico** (`caminho_bach_chopin.csv`, 50 compositores):
- Mais perto do segmento: Mozart (t = 0,30; dist. 0,288), Tchaikovsky (0,77; 0,325), Beethoven (0,39; 0,327), Schubert (0,76; 0,334), Grieg (0,92; 0,335).
- Dentro do segmento (0 < t < 1, 42 compositores), t × nascimento: ρ = 0,53.
- A distância ao segmento vai de 0,288 a 0,947 (média 0,477).

**(b) Steering forte** (progresso médio ± erro padrão, n = 14 por condição, calculado de `steering_forte.csv`):

| condição | α | progresso | repetição de trigramas |
|---|---|---|---|
| nenhum | 0 | 0,392 ± 0,034 | 0,041 |
| aleatório | 1 | 0,433 ± 0,038 | 0,032 |
| centrado | 1 | 0,684 ± 0,024 | 0,028 |
| caminho t = 0 | 1 | 0,277 ± 0,016 | 0,024 |
| caminho t = 0,5 | 1 | 0,338 ± 0,026 | 0,017 |
| caminho t = 1 | 1 | 0,688 ± 0,022 | 0,015 |

- Distância cosseno média ao centróide de Chopin: nenhum 1,182; centrado 0,930.
- Piloto (n = 6): centrado α = 0,2 → 0,550; α = 0,5 → 0,578; α = 1 → 0,741. Aleatório α = 0,5 → 0,479; nenhum → 0,406.

## Comparação com o nulo
- Por semente (média das 2 amostras, 7 sementes, calculado do CSV): centrado > aleatório em 7 de 7 (Wilcoxon p = 0,016, o menor possível com 7 pares) e centrado > nenhum em 7 de 7 (p = 0,016).
- Aleatório > nenhum em 4 de 7 sementes (p = 0,30): o vetor aleatório não se distingue de não fazer steering.

## O que não se pode concluir
- **H6 se confirma no ponto α = 1**: centrado (0,68) fica acima de aleatório (0,43) e de nenhum (0,39). A parte "monótona em α até a quebra" só tem o piloto (3 sementes, 3 valores de α, sem α > 1). Não se viu a quebra.
- **H7:** t = 0 → 0,28, t = 0,5 → 0,34, t = 1 → 0,69. É monótono, mas não linear. O ponto médio (0,34) fica abaixo do "nenhum" (0,39), então só t = 1 supera a continuação sem steering. O vetor de Bach sozinho (t = 0) reduz o progresso. A pergunta sobre os intermediários ficarem perto dos clássicos não foi respondida pelo steering, só pela geometria (a).
- t = 1 e "centrado" são o mesmo vetor; a diferença (0,688 contra 0,684) mostra o ruído da geração.
- Progresso 0,68 é a projeção num eixo, não chegar a Chopin. A distância ao centróide de Chopin continua grande (0,930; a distância média entre centróides é 0,942) e a distância a Bach também aumenta (1,00, contra 0,79 sem steering).
- A projeção usa o eixo Bach → Chopin, a mesma direção que o vetor centrado empurra. Seria mais forte conferir com outros alvos e outras métricas.
- Um par de compositores, sementes só de Bach, 7 sementes. As 2 amostras por semente não são independentes. Sem julgamento de áudio nem verificação auditiva.
- A repetição de trigramas ficou ≤ 4% em todas as condições. Isso não exclui outros defeitos na música gerada.
- (a): ρ = 0,53 entre t e nascimento é moderado. Scriabin (t = 1,08) e Debussy (t = 1,02) projetam além de Chopin. Não há nulo para a distância ao segmento.

## Figuras
- [Progresso por condição de steering](figs/steering.png)

## Ideias fora do escopo
- Grade completa de steering: outros pares, α > 1, mais sementes.
- Outros eixos de medida (distância ao centróide em vez de projeção).
- Avaliação auditiva do que é gerado (fora do escopo do ensaio).
- Mais pontos no caminho (t = 0,25; 0,75).
