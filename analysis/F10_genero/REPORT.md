# F10 — É época ou é gênero? (B1)

Base sem duplicatas (08/11): números atualizados; conclusões inalteradas.

## Pergunta
A organização cronológica do mapa de compositores se deve ao gênero das peças (fugas antes, noturnos depois)?

## Hipótese registrada
- **H12:** a cronologia sobrevive ao controle de gênero (Mantel ρ > 0,3) e o bloco pré-romântico {Bach, Handel, Scarlatti, Haydn, Mozart, Beethoven, Hummel} continua.

## Configuração
- Camada 6, pooling média, janelas 1 e 2; 52 compositores, 2.103 peças (nível de peça, centrado, l2norm, como em F3).
- Gênero por regex do título (dicionário GEN de F4); "outro" é a categoria de referência. Contagens: outro 1.103; sonata 335; dança/minueto 96; prelúdio 91; valsa 80; estudo 61; variações 56; rag 40; mazurca 45; noturno 41; romance/canção 35; suíte 32; fuga 30; marcha 24; improviso 20; rapsódia 13; tango/choro 1.
- Regressão de mínimos quadrados das representações das peças no one-hot de gênero, com intercepto; resíduos re-normalizados (l2norm). O gênero explica 8,3% da variância das representações das peças.
- Com os resíduos: centróides por compositor, distância cosseno, Mantel (Spearman, 5.000 permutações) contra |Δ nascimento|, R² do compositor (como em F4) e divisão k = 2 por ligação média (como em F5).
- Base de comparação recalculada no mesmo script (reproduz H1 e R² anteriores).

## Resultado
| | Sem controle | Resíduos de gênero |
|---|---|---|
| Mantel ρ (p) | 0,502 (0,0002) | **0,374** (0,0002) |
| R² do compositor | 0,268 | **0,194** |
| k = 2 | {7 pré-românticos} vs. 45 | 25 vs. 27 |

- Spearman entre as matrizes de distância (base × resíduos): 0,91.
- **Cronologia:** sobrevive (ρ = 0,37 > 0,3), mas cai cerca de 25% do valor original.
- **Bloco pré-romântico, k = 2:** na base, o k = 2 isola exatamente os sete compositores. Nos resíduos, os sete continuam juntos no mesmo ramo, mas o corte em dois grupos mudou: o grupo de Bach tem 27 compositores (inclui também Alkan, Czerny, Gottschalk, Gurlitt, Heller, Hitz, J. Scott, Johnson, Joplin, Mendelssohn, Moszkowski, Nazareth, Raff, Ravina, Satie, Schubert, Tchaikovsky, Teilman, Victoria, Wachs: 20 a mais que os sete) e o outro tem 25 (Balakirev, Brahms, Busoni, Chaminade, Chopin, Debussy, Fauré, Godard, Grieg, Lack, Lange, Liszt, Medtner, Meyer-Helmund, Poulenc, Prokofiev, Rachmaninoff, Rebikov, Rzewski, Scharwenka, Schumann, C. Scott, Scriabin, Turina, Villa-Lobos). Ou seja, o bloco permanece coeso, mas deixa de ser um grupo isolado; o corte em k = 2 passa a separar um grupo "mais sóbrio/antigo" de um "mais tardio-romântico/moderno".
- **H12:** a primeira parte (ρ > 0,3) confirmada. A segunda ("o bloco continua") só vale na leitura fraca (os sete seguem juntos); não vale na forte (o k = 2 não o isola mais).

## Comparação com o nulo
Mantel: p vem de permutar a ordem dos compositores; 0,0002 = 1/5001 é o mínimo possível. Não há nulo próprio para a divisão k = 2.

## O que não se pode concluir
- O gênero é medido por regex no título e 52% das peças (1.103 de 2.103) caem em "outro"; o controle é parcial e subestima o efeito real de gênero. Peças de títulos genéricos (ex.: "Op. 10 No. 3") são tratadas como um só gênero.
- Gênero e época são correlacionados (fuga é barroca, noturno é romântico): remover o gênero remove também parte legítima do sinal de época. A queda de ρ não distingue "gênero confundindo" de "gênero como parte do estilo da época".
- A regressão é linear e remove só deslocamentos médios por gênero, não interações compositor × gênero.
- Tango/choro tem uma única peça, e o coeficiente é praticamente não identificado.
- A estabilidade do k = 2 não foi testada por bootstrap aqui.

## Figuras
Nenhuma.

## Ideias fora do escopo
- Controlar gênero e descritores de superfície (A3) simultaneamente.
- Bootstrap do k = 2 sob resíduos; classificar gênero por conteúdo e não por título.
