# F5 — Forma do espaço (Q3)

## Pergunta
O espaço dos compositores tem grupos separados ou é um contínuo?

## Hipótese registrada
**H5:** o espaço é um contínuo; se houver um ramo destacado, ele é o Barroco.

## Configuração
- Camada 6, pooling média; 52 centróides, distância cosseno. Peças com 2 janelas (passada 2, números finais do ensaio).
- Homologia persistente de grau 0 (barras = alturas de fusão da ligação simples).
- Nulo: 200 gaussianas com a mesma média e covariância dos centróides (sem grupos). Estatística: razão entre a maior barra e a mediana.
- Estabilidade: dendrograma de ligação média cortado em k = 2 a 5; ARI médio em 100 bootstraps por peças.

## Resultado
- Maior barra de H0: 0,515. Mediana das barras: 0,291. Razão: 1,769.
- ARI bootstrap: k = 2: 0,782; k = 3: 0,436; k = 4: 0,567; k = 5: 0,565.
- **Passada 1 (1 janela), para comparar:** razão 1,601 (p95 do nulo 2,274); ARI k = 2: 0,787, k = 3: 0,557, k = 4: 0,569, k = 5: 0,556. O corte em 2 grupos tem a mesma composição e o mesmo ARI (~0,78–0,79). A razão subiu (1,60 → 1,77) mas continua abaixo do p95 do nulo (2,31).
- Corte em 2 grupos:
  - Grupo 1 (7): Bach, Beethoven, Handel, Haydn, Hummel, Mozart, Scarlatti.
  - Grupo 2 (45): todo o resto, inclusive Victoria.
- Corte em 3: o grupo 2 se divide em {Gurlitt, Rebikov, Satie, Victoria} e o restante (41). Na passada 1, o corte em 3 separava outro bloco (Alkan, Busoni, Czerny, Johnson, Joplin, Moszkowski, Nazareth, Raff, Schubert, J. Scott), e aquele grupo de quatro só surgia em k = 4.
- Corte em 4: o restante se divide em 25 e 16; o bloco de 16 tem Alkan, Czerny, Godard, Gottschalk, Hitz, Johnson, Joplin, Lange, Meyer-Helmund, Nazareth, Raff, Ravina, Schubert, J. Scott, Teilman e Wachs.

## Comparação com o nulo
Razão observada 1,769, contra p95 do nulo 2,31. Não há lacuna maior do que a de uma nuvem gaussiana sem grupos.

## O que não se pode concluir
- H5 (contínuo) é compatível com os dados: não há separação além do nulo. Isso não prova que não existam grupos; com 52 pontos, o teste tem pouca potência.
- "O ramo destacado é o Barroco" se confirma só em parte. O grupo estável de 2 não é só Barroco: inclui Clássicos (Haydn, Mozart, Beethoven, Hummel). Descrever como "pré-romântico".
- A divisão em 2 é estável (0,78); as de 3 a 5 não (0,44 a 0,57). Os grupos finos mudaram entre as passadas 1 e 2 (k = 3 e k = 4 trocaram de composição); não interpretar.
- Os grupos vêm da ligação média, e o teste de lacuna da ligação simples. São dois procedimentos; o ARI mede só o primeiro.
- O nulo gaussiano preserva a covariância, mas não a forma real da distribuição.
- Só grau 0. Nada foi medido sobre ciclos (grau 1) ou Mapper.
- As listas usam só o sobrenome; "Scott" aparece duas vezes (J. e C. Scott).

## Figuras
- [Dendrograma](figs/dendrograma.png)
- [Barras de H0 contra o nulo](figs/h0_barras.png)

## Ideias fora do escopo
- Mapper e homologia de grau 1 (previstos como "depois").
- Repetir com a janela da passada 3 (5/6) e conferir se o grupo "pré-romântico" se mantém (já se manteve da passada 1 para a 2).
- Nulo que preserve a estrutura cronológica.
