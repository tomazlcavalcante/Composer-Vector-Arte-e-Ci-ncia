# F5 — Forma do espaço (Q3)

Base sem duplicatas (08/11): números atualizados; conclusões inalteradas.

## Pergunta
O espaço dos compositores tem grupos separados ou é um contínuo?

## Hipótese registrada
**H5:** o espaço é um contínuo; se houver um ramo destacado, ele é o Barroco.

## Configuração
- Camada 6, pooling média; 52 centróides, distância cosseno. 2.103 peças com 2 janelas (passada 2, números finais do ensaio; sem as 80 cópias).
- Homologia persistente de grau 0 (barras = alturas de fusão da ligação simples).
- Nulo: 200 gaussianas com a mesma média e covariância dos centróides (sem grupos). Estatística: razão entre a maior barra e a mediana.
- Estabilidade: dendrograma de ligação média cortado em k = 2 a 5; ARI médio em 100 bootstraps por peças.

## Resultado
- Maior barra de H0: 0,553. Mediana das barras: 0,290. Razão: 1,911 (p95 do nulo 2,376).
- ARI bootstrap: k = 2: 0,787; k = 3: 0,682; k = 4: 0,715; k = 5: 0,726.
- **Passada 1 (1 janela, base com cópias), para comparar:** razão 1,601 (p95 do nulo 2,274); ARI k = 2: 0,787, k = 3: 0,557, k = 4: 0,569, k = 5: 0,556. O corte em 2 grupos tem a mesma composição e o mesmo ARI (0,787). A razão subiu (1,60 → 1,91) mas continua abaixo do p95 do nulo (2,38). Sem as cópias, o ARI de k = 3 a 5 subiu (0,68 a 0,73), mas segue abaixo do de k = 2.
- Corte em 2 grupos:
  - Grupo 1 (7): Bach, Beethoven, Handel, Haydn, Hummel, Mozart, Scarlatti.
  - Grupo 2 (45): todo o resto, inclusive Victoria.
- Corte em 3: o grupo 2 se divide em um bloco de 10 {Alkan, Czerny, Hitz, Johnson, Joplin, Nazareth, Raff, Schubert, J. Scott, Wachs} e o restante (35). É quase o bloco que a passada 1 separava em k = 3 (lá com Busoni e Moszkowski, sem Hitz e Wachs).
- Corte em 4: o restante se divide em {Gurlitt, Rebikov, Satie, Victoria} (4) e 31 compositores; o bloco de 10 se mantém.

## Comparação com o nulo
Razão observada 1,911, contra p95 do nulo 2,38. Não há lacuna maior do que a de uma nuvem gaussiana sem grupos.

## O que não se pode concluir
- H5 (contínuo) é compatível com os dados: não há separação além do nulo. Isso não prova que não existam grupos; com 52 pontos, o teste tem pouca potência.
- "O ramo destacado é o Barroco" se confirma só em parte. O grupo estável de 2 não é só Barroco: inclui Clássicos (Haydn, Mozart, Beethoven, Hummel). Descrever como "pré-romântico".
- A divisão em 2 é estável (0,79); as de 3 a 5 são menos estáveis (0,68 a 0,73, contra 0,44 a 0,57 antes de remover as cópias). Os grupos finos mudaram entre as passadas 1 e 2 e de novo sem as cópias; não interpretar até reavaliar o veredito de k ≥ 3.
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
