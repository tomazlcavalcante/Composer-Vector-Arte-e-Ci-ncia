# Resultados

Ensaio para Artes e Ciência (IMPA Tech). Este texto reúne o que o estudo encontrou, o que se sustenta e o que não se pode concluir. Os números vêm dos `metrics*.json`, dos CSVs e dos REPORTs corrigidos (errata do DIARIO). Quando DIARIO e REPORT divergem, vale o REPORT. O filtro de validade é `analysis/F6_controles/VALIDADE.md`.

## Abertura

Pegamos um modelo que aprendeu a prever música, o Anticipatory Music Transformer small, treinado no Lakh MIDI. Pedimos a ele a "impressão digital" de 2.103 peças de piano do acervo GiantMIDI, de 52 compositores, e fizemos a média por compositor. Em seguida olhamos como o modelo organiza esses compositores no seu espaço interno. A resposta principal: o modelo organiza os compositores de forma parcialmente cronológica, com um bloco pré-romântico (Bach a Beethoven) à parte, mas sem grupos nítidos. O compositor explica só uma minoria (27%) da variação entre peças, então o estilo, nesse espaço, é mais nuvem do que ponto. Somar o vetor de Chopin aumenta, de forma parcial, a projeção da música gerada no eixo Bach → Chopin (mais do que um vetor aleatório). Testado em 4 pares, o efeito vale em 3 de 4 direções interpretáveis, todas entre compositores distantes, e falha em Joplin → Chopin. A cronologia sobrevive quando se retiram as estatísticas simples de superfície (Mantel ρ de 0,502 para 0,356) e o gênero do título (0,374), então o modelo capta mais do que densidade, registro ou forma, embora perca de um quarto a um terço do ρ. Em análise exploratória e com poucas peças, as valsas de Nazareth, Joplin e Johnson caem perto de Chopin e longe do ragtime, ao contrário dos tangos e polcas de Nazareth: um indício de que a "valsa" atravessa autores no mapa do modelo, sem que pareça ser só o compasso (F14), mas com n pequeno. Há um explorador interativo do mapa: https://claude.ai/artifact/NeP4zc74AncnZsXsZuLvvo.

## Base de dados

Em 08/11 removemos 80 cópias da base: eram 37 grupos de MIDIs idênticos byte a byte (117 peças), a mesma gravação sob títulos diferentes, concentrados em Meyer-Helmund, Handel e Godard (lista em `analysis/data/duplicatas_remover.txt`, aplicada na leitura comum). A base passou de 2.183 para 2.103 peças. Todos os números abaixo vêm das análises refeitas sem as cópias (F2–F5, F8–F11, F14 e as valsas da F13), e as conclusões não mudaram. **F6 (transposição) e F7 (steering) são da base anterior** (não foram refeitas). Os `metrics.json` da F12 (finais de obra) e da F13 (parte descritiva) foram regerados com 2.103 peças e entram abaixo com os números novos (os REPORTs dessas duas pastas ainda trazem os números antigos). Os números das comparações "passada 1" (1 janela) também são da base com cópias.

## Como ler os vereditos

- **Sobrevive:** nenhum controle ameaça a afirmação.
- **Enfraquece:** vale, com ressalva.
- **Cai:** não se sustenta.
- "Camada 6, média" é a representação escolhida na F2 (a menos que se diga outra).

## Q0. Qual representação do modelo usar? (F2)

**Resposta.** As camadas do meio separam melhor os compositores do que a última, e a média da janela é melhor do que o último token.

**Números.**
- Acurácia balanceada (regressão logística, 5 dobras, divisão por peça; 52 classes): camada 6 com média = 0,311; camada 12 (última) com média = 0,186. Último token: 0,166 na camada 5 e 0,057 na 12.
- Acaso = 1/52 = 0,019. Todas as camadas com média ficam acima (mínimo 0,136, camada 0).
- Estabilidade dos centróides (duas metades das peças): 0,829 na camada 6.
- Sem intervalo de confiança nem nulo por permutação: cada número é uma execução.

**Veredito.** A hipótese da F2 (camadas intermediárias ≥ última) se confirma na direção. Não é uma linha da VALIDADE; a ressalva está no REPORT da F2.

**O que NÃO se pode concluir.**
- Que a camada 6 é melhor que a 5, 7, 8 ou 9: as camadas 5 a 9 estão empatadas (acurácia de 0,299 a 0,311; a 8, com 0,311, empata com a 6), sem intervalo. Pelo critério (acurácia + estabilidade) a melhor é a 7 (1,150 contra 1,139 da 6; diferença de 0,010). **Mantida a camada 6**: a escolha foi feita antes da descoberta das duplicatas, e a regra, escrita no `run.py`, é mantê-la se estiver a até 0,02 da melhor, para não reabrir a escolha depois de ver os dados. A 5 é a secundária.
- Que o modelo "sabe" menos na última camada: a camada 12 pode estar especializada em prever o próximo token (interpretação, não testada).
- Acurácia de 0,31 em 52 classes está bem acima do acaso, mas é baixa em termos absolutos.
- A camada foi escolhida e avaliada nos mesmos dados.

## Q1. Quem fica perto de quem? (F3)

**Resposta.** Compositores de épocas próximas ficam mais perto no espaço do modelo, mas a relação é moderada; a nacionalidade não mostra efeito detectável quando se controla a época, nem dentro dos românticos.

**Números.**
- Distância entre centróides × diferença de ano de nascimento (H1): Mantel ρ = 0,502, p = 0,0002 (5.000 permutações; é o menor p possível). Em outras representações, ρ = 0,49 (camada 5), 0,42 (camada 12) e 0,415 (último token); todas com p ≤ 0,001 (1.000 permutações).
- Nacionalidade (H2): ρ = 0,082 (p = 0,020); controlando a época, ρ = 0,040 (p = 0,116). Nas outras configurações o ρ parcial fica entre 0,01 e 0,04, sem intervalo.
- Nacionalidade dentro dos românticos (H18, F16; 33 compositores, 528 pares, 72 de mesma nacionalidade): Mantel parcial, controlando |Δ nascimento|, ρ = −0,01 (−0,007), p unicaudal = 0,52 (nulo: p95 = 0,094). Francês, alemão e russo não são mais coesos que a média. Poder baixo.
- Controle de transposição: mover a peça ±2 ou ±5 semitons desloca o vetor em 0,022–0,027, contra 0,93 entre centróides (45 peças, 1 janela, sem nulo nem intervalo; F6, base anterior).
- Mapa 2D (PCA): PC1 explica 33,8% e PC2 19,3% da variância dos centróides. PC1 × ano de nascimento: ρ = 0,499 (PC2 × ano não foi recalculado; era 0,26 na base anterior). O mapa distorce as distâncias reais (Spearman 0,75).
- Vizinhos mais próximos (ilustração; os IC são largos): Haydn ↔ Mozart 0,107 [0,087; 0,213]; J. Scott ↔ C. L. Johnson 0,075 [0,063; 0,113]; Bach ↔ Handel 0,175 [0,122; 0,288], agora mútuo (o segundo vizinho de Bach é Scarlatti, 0,202); Chopin ↔ Grieg 0,319 [0,266; 0,597], também mútuo. Debussy → C. Scott (0,172 [0,126; 0,425]) não é mútuo (o vizinho de C. Scott é Turina, 0,164). Medtner → Rachmaninoff (0,233 [0,195; 0,492]); Medtner–Schumann (0,239 [0,224; 0,485]) deixou de ser o par mais próximo. Satie → Rebikov (0,289 [0,208; 0,458]) não é mútuo (o vizinho de Rebikov é Scharwenka).
- Tico-Tico (uma peça): vizinhos C. L. Johnson (0,417), J. Scott (0,444), Nazareth (0,489).

**Veredito.**
- Época (H1): **sobrevive**.
- Nacionalidade (H2): **sobrevive, com cautela** (ausência de evidência, não evidência de ausência; teste de pouca potência; metadados não verificados fora). Dentro dos românticos (H18, VALIDADE linha 19): também sem efeito (ρ parcial −0,01, p = 0,52), com a mesma cautela.
- Vizinhos com sentido musical: **enfraquece** (muitos pares mudam entre 1 e 2 janelas; pares individuais não têm teste). Usar como ilustração.
- Tico-Tico ao lado do ragtime: **ilustração**, não resultado (só os 3 primeiros vizinhos se mantêm entre 1 e 2 janelas).
- Transposição: **enfraquece** (13 de 45 peças, 29%, trocam de centróide mais próximo em alguma transposição; 17 de 180 linhas, 9,4%).

**O que NÃO se pode concluir.**
- Que a cronologia explica a ordem: ρ = 0,50 é moderado. O mapa "acompanha, em parte, a cronologia"; não é uma linha do tempo.
- Que a nacionalidade não importa.
- Que a tonalidade é irrelevante para o mapa.
- Que dois vizinhos se parecem por razão musical: a distância não diz se a causa é harmonia, textura, gênero, forma do arquivo MIDI ou a gravação.
- A lista de "afinidades inesperadas" (resíduo linear) é dominada por Victoria, a 300 anos de distância. Não é achado.

## Q2. Ponto ou nuvem? (F4)

**Resposta.** O compositor explica uma minoria da variação entre peças; a música de um compositor forma uma nuvem que se sobrepõe à de outros.

**Números.**
- R² do compositor (H3) = 0,268. Nulo (200 permutações de rótulos): média 0,0243, p95 0,0267. Nas outras representações, R² de 0,26 (camada 5), 0,21 (camada 12) e 0,12 (último token).
- 66,9% das peças ficam mais perto do centróide de outro compositor. Mesmo assim, o acerto médio por compositor é 0,337, contra cerca de 0,019 ao acaso.
- Gênero (H4; 1.000 peças com gênero por palavra-chave do título): R² do gênero = 0,155, do compositor nas mesmas peças = 0,303. Distância média: mesmo compositor e gênero diferente 0,779; mesmo gênero e compositor diferente 0,944.
- Mais compactos (n igualado em 20): Victoria 0,084, C. L. Johnson 0,251, J. Scott 0,297, Meyer-Helmund 0,318, Joplin 0,423. Meyer-Helmund agora tem só 6 peças (as demais eram cópias) e é reamostrado com reposição até 20, então sua compacidade pesa pouco. Mais espalhados: Heller 0,902, Ravina 0,894, Gurlitt 0,884, Mendelssohn 0,876, Hummel 0,8745 (Moszkowski vem a seguir, 0,8675).
- Dentro da obra: janelas da mesma peça ficam a 0,438 uma da outra; peças diferentes do mesmo compositor, a 0,794; compositores diferentes, a 1,005. Em 52 de 52 compositores, as janelas da mesma peça ficam mais próximas entre si do que de outras peças do mesmo compositor (diferença 0,33, IC95% 0,30–0,36).
- R² bruto "da peça" = 0,78 (0,7809), mas o nulo por construção (2 janelas por peça) é 0,50; corrigido, (0,7809 − 0,50)/(1 − 0,50) = 0,56. O nulo de 0,50 vem da fórmula (G−1)/(N−1), não de arquivo. Não comparar com o R² do compositor.

**Veredito.**
- Compositor explica minoria (H3): **sobrevive** (o número exato depende da representação, de 0,12 a 0,27; é sempre uma minoria bem acima do nulo).
- Compositor pesa mais que gênero (H4 não se confirma): **enfraquece** (R² não ajustado pelo número de grupos, gênero por título é impreciso, sem intervalo).
- Obra mais coesa que o compositor: **enfraquece** (confundido com gravação e arquivo MIDI, que são os mesmos nas duas janelas).
- "Originalidade" = distância bruta à média geral; o número de peças correlaciona pouco com ela (ρ = −0,174). O z de originalidade cresce com n por construção (ρ = 0,487) e não deve ser usado.

**O que NÃO se pode concluir.**
- Que o compositor não é identificável: 31% de acerto em 52 classes (sonda) é muito acima do acaso.
- Que os 73% restantes são "variação de estilo da obra": incluem gênero, forma, tonalidade e ruído de transcrição, sem decomposição.
- Que Victoria e os ragtimes têm estilo mais coeso: a compacidade pode vir do tipo de arquivo MIDI (não testado). Victoria tem exatamente 20 peças, e Meyer-Helmund, só 6.
- A ordem dos mais espalhados é instável (mudou entre 1 e 2 janelas por peça e de novo sem as cópias: Moszkowski saiu e Hummel entrou); os mais compactos são os mesmos cinco.
- As obras atípicas (a mais atípica: "Wedding of the Fairies Waltz" de Johnson, z = 4,47) são só para leitura qualitativa.

## Q3. Grupos ou contínuo? (F5)

**Resposta.** O espaço é um contínuo, com um corte claro: os sete compositores pré-românticos de um lado e os outros 45 do outro. Sem as cópias, aparecem também regiões finas estáveis dentro dos 45, mas exploratórias e sem fronteira de ilha.

**Números.**
- Maior barra de H0 = 0,553; mediana = 0,290; razão = 1,911, contra p95 do nulo gaussiano de 2,38. Não há lacuna maior do que a de uma nuvem sem grupos (200 gaussianas).
- Corte em 2 grupos (ligação média): ARI em 100 bootstraps de peças = 0,787. Grupo de 7: Bach, Beethoven, Handel, Haydn, Hummel, Mozart, Scarlatti. Grupo de 45: todo o resto, inclusive Victoria.
- Cortes em 3, 4 e 5: ARI = 0,682, 0,715 e 0,726 (contra 0,44–0,57 antes de remover as cópias; ainda abaixo do corte em 2, 0,787). Com k = 3, os 45 se dividem em um bloco "regular e dançante" de 10 (Alkan, Czerny, Hitz, Johnson, Joplin, Nazareth, Raff, Schubert, J. Scott, Wachs) e os 35 restantes; com k = 4 surge o grupo "despojado" (Gurlitt, Rebikov, Satie, Victoria). Não foram previstos: surgiram depois da limpeza dos dados, então são exploratórios. A razão da lacuna (1,911 contra p95 de 2,38) continua dizendo contínuo: são regiões de um contínuo, não ilhas.
- Nas camadas 5 e 6 o bloco é o mesmo; nas camadas 12 e com último token ele vem com intrusos (Victoria, ragtime).

**Veredito.** Contínuo e bloco pré-romântico: **sobrevive**. Grupos mais finos (k ≥ 3): **enfraquece**, exploratório (antes **cai**; ficaram estáveis sem as cópias, mas não foram previstos e não são ilhas). A robustez do bloco entre representações é parcial.

**O que NÃO se pode concluir.**
- Que não existem grupos: com 52 pontos o teste tem pouca potência.
- Que o ramo destacado é "o Barroco" (H5): o grupo inclui Clássicos. Chamar de pré-romântico.
- Que os grupos finos são reais: surgiram depois da limpeza, vêm só da ligação média e os nomes ("regular e dançante", "despojado") são nossos.
- Nada sobre ciclos (grau 1) ou Mapper: só foi medido o grau 0.
- Os grupos vêm da ligação média e o teste de lacuna, da ligação simples; o ARI mede só o primeiro. O nulo gaussiano não preserva a forma real da distribuição.

## Q4. Somar o vetor de um compositor desloca a música? (F7)

*Base anterior (2.183 peças): o steering não foi refeito; as gerações não dependem da base, e o efeito sobre os centróides é desprezível, segundo o DIARIO.*

**Resposta.** Somar o vetor centrado de Chopin na camada 6 aumenta a projeção da continuação, relida sem steering, no eixo Bach → Chopin, mais do que um vetor aleatório ou nenhum vetor. O deslocamento é parcial e vale em 3 de 4 direções interpretáveis (ver "Outros pares").

**Números** (progresso: 0 = centróide de Bach, 1 = centróide de Chopin; média ± erro padrão).
- α = 1, n = 14 (7 sementes de Bach × 2 amostras, centróides de 1 janela): nenhum 0,392 ± 0,034; aleatório 0,433 ± 0,038; centrado 0,684 ± 0,024.
- Por semente (7): centrado > aleatório em 7 de 7 (Wilcoxon p = 0,016, o menor possível) e centrado > nenhum em 7 de 7 (p = 0,016). Aleatório > nenhum em 4 de 7 (p = 0,30).
- Varredura de α (7 sementes × 1 amostra, centróides de 2 janelas), centrado: 0,382 (α = 0), 0,474 (0,25), 0,585 (0,5), 0,682 (1), 0,755 (1,5). Aleatório: entre 0,38 e 0,47, sem tendência. A média sobe com α, mas por semente só 4 de 7 trajetórias são monótonas.
- Na varredura (centróides de 2 janelas), a distância ao centróide de Chopin cai de 1,178 (nenhum) para 0,849 (centrado, α = 1,5). A distância a Bach sobe de 0,758 para 1,074.
- Caminho (1−t)·v_Bach + t·v_Chopin: t = 0 → 0,277; t = 0,5 → 0,338; t = 1 → 0,688. Monótono, não linear. O ponto médio fica abaixo de "nenhum" (0,392).
- Sentido inverso Chopin → Bach (n = 7, centróides de 2 janelas): centrado 0,461 ± 0,035; nenhum 0,325; aleatório 0,287. Centrado > ambos em 7 de 7 (p = 0,016). Ganho sobre "nenhum": +0,136, contra +0,292 de Bach para Chopin.
- Geometria (50 compositores, centróides de 1 janela): Mozart (t = 0,30; distância 0,288) e Beethoven (t = 0,39; 0,327) são os clássicos mais próximos do segmento Bach → Chopin. Dentro do segmento (42 compositores), t × nascimento: ρ = 0,53.
- Repetição de trigramas (única medida de degeneração): médias de 1,5% a 4,1% no experimento principal; sem aumento sistemático até α = 1,5. Máximo por continuação: 28,9% (principal), 23,7% (varredura), 39,5% (inverso).

**Veredito.**
- Efeito do vetor centrado (H6): **sobrevive**, como deslocamento parcial.
- Descritores independentes: H19 **parcial**, H20 **mista** (VALIDADE, linhas 20 e 21).
- Progresso monótono no caminho Bach → Chopin (H7): **enfraquece** (o caminho só foi testado em Bach ↔ Chopin; 7 sementes).

**O que NÃO se pode concluir.**
- Que a música "virou Chopin": o progresso de 0,68 é a projeção num eixo, e a distância ao centróide de Chopin continua em 0,930 (α = 1, experimento principal; 1,182 sem steering).
- Que "Bach domina a mistura": a observação é descritiva, sem teste. A diferença entre t = 0,5 (0,338) e "nenhum" (0,392) é menor que 2 erros padrão.
- Que o efeito é menor no sentido inverso por causa do vetor: a comparação mistura eixos, sementes, bases de centróides (1 contra 2 janelas) e n (14 contra 7). As continuações de Chopin sem steering repetem mais trigramas (0,124 contra 0,041).
- Que não há quebra: não vimos aumento da repetição até α = 1,5, mas isso não garante música coerente. Não houve escuta nem outro eixo; outros pares e descritores independentes aparecem abaixo, com 7 sementes. O eixo de medida é o mesmo que o vetor centrado empurra.
- Que os pontos intermediários caem perto dos clássicos: isso só foi visto na geometria, não no steering.

**Outros pares** (`analysis/F7_deslocamento/pares_resumo.csv`; 7 sementes, 1 amostra por condição, α = 1, centróides de 2 janelas, exceto Bach → Chopin, que usa a base "forte" de 1 janela):

| Par | Distância entre centróides | Nenhum | Aleatório | Centrado | Centrado > aleatório |
|---|---|---|---|---|---|
| Bach → Chopin | 1,60 | 0,39 | 0,43 | 0,68 | 7/7 (p = 0,016) |
| Chopin → Bach | 1,60 | 0,33 | 0,29 | 0,46 | 7/7 (p = 0,016) |
| Mozart → Debussy | 1,71 | 0,22 | 0,28 | 0,50 | 6/7 (p = 0,031) |
| Joplin → Chopin | 1,11 | 0,44 | 0,49 | 0,54 | 5/7 (p = 0,69) |
| Haydn → Mozart | 0,10 | — | — | — | não interpretável |

O efeito se repete em 3 das 4 direções interpretáveis e falha em Joplin → Chopin. Haydn e Mozart estão quase sobrepostos no mapa (distância de 0,10), então o eixo "origem → alvo" não está bem definido e o progresso sai do intervalo 0–1. **Leitura:** H6 deixa de depender de um par só, mas não vale para qualquer par. Nos três pares em que funcionou, os compositores estão distantes no mapa (distância ≥ 1,6). Com 4 pares, a relação entre distância e efeito é só sugestiva.

**Checagem com descritores independentes do modelo** (`analysis/F7_deslocamento/metrics_descritores.json`; 7 sementes de Bach × 2 amostras, continuações de 40 notas, vetor centrado de Chopin com α = 1). Medimos a música gerada sem usar o modelo, com estatísticas simples das notas. O resultado é misto:
- **Vão na direção de Chopin:** a duração média das notas sobe de 0,30 s para 0,65 s em 7 de 7 sementes (referência: Bach 0,37 s, Chopin 0,63 s). A polifonia sobe de 2,4 para 3,0 (6 de 7 contra a condição sem steering; 7 de 7 contra o aleatório). A dispersão das alturas aumenta em relação ao vetor aleatório (7 de 7).
- **Vão contra:** as notas por segundo caem de 9,0 para 4,8 (7 de 7), embora Chopin seja mais denso que Bach na referência (9,3 contra 8,0). A altura média cai cerca de 3 semitons.
- **Leitura cautelosa:** o vetor muda de fato a textura (notas mais longas, mais sobrepostas, música mais "lenta"), e parte dessa mudança coincide com o perfil de Chopin. Mas não é uma imitação de Chopin em todos os aspectos. Com 7 sementes, um só par (Bach → Chopin) e descritores simples, isso é indício, não prova.

**Descritores em mais dois pares** (H19 e H20; `analysis/F7_deslocamento/metrics_descritores_Mozart_Debussy.json` e `..._Chopin_Joplin.json`; mesmo procedimento: 7 sementes × 2 amostras, continuações de 40 notas, α = 1; entra a entropia de classes de altura, que mede o cromatismo). Médias sem steering ("nenhum") → vetor centrado:

| Par | Duração média (s) | Notas por s | Polifonia | Entropia de classes (bits) |
|---|---|---|---|---|
| Bach → Chopin | 0,30 → 0,65 | 9,04 → 4,84 | 2,38 → 2,95 | não medida |
| Mozart → Debussy | 0,29 → 1,05 | 9,52 → 7,04 | 2,37 → 4,59 | 2,76 → 2,66 |
| Chopin → Joplin | 0,30 → 0,26 | 15,33 → 18,48 | 3,56 → 4,24 | 2,23 → 2,49 |

- **H19 (Mozart → Debussy): parcial.** Polifonia e duração vão na direção de Debussy em 7 de 7 sementes contra os dois controles (p = 0,016). A entropia de classes não: 1 de 7 contra "nenhum" e 4 de 7 contra o aleatório (p ≥ 0,22).
- **H20 (Chopin → Joplin, alvo de perfil oposto): mista.** As notas por segundo **sobem**, na direção de Joplin e ao contrário dos outros dois pares (7 de 7 contra o aleatório, p = 0,016; 5 de 7 contra "nenhum", p = 0,078). A duração deixa de subir (0,30 → 0,26 s; p = 0,30). A polifonia sobe nos três pares, mesmo quando o alvo tem menos (Joplin: 2 de 7 sementes na direção dele). A entropia de classes não se distingue do aleatório em nenhum dos dois pares (4 de 7, p = 0,81; 2 de 7, p = 0,58).
- **Leitura:** o efeito sobre o andamento (duração e notas por segundo) depende do alvo; o aumento da polifonia parece um efeito comum do steering; o cromatismo não se move de forma distinguível nos dois pares em que foi medido. Ressalvas: 7 sementes (p mínimo 0,016), vários testes sem correção, amostras não independentes, continuação de 40 notas, só uma camada e um α, sem escuta; contra "nenhum", nem a duração nem as notas por segundo de Joplin chegam a p < 0,05.
- Figura de apoio: `analysis/F7_deslocamento/figs/descritores_tres_pares.png` (centrado − nenhum, para duração e notas por segundo, nos três pares; a polifonia e a entropia não estão na figura).

## Q5. Expectativa: o quanto o modelo se surpreende? (F8)

**Resposta.** A surpresa do modelo varia entre compositores e cresce, em média, com a época; isso é surpresa **para este modelo**, não expectativa de um ouvinte.

**Números** (perda média por token, em nats).
- Média das peças: 2,49 (dp 0,48 entre peças; 0,31 entre compositores). Menor: Victoria 1,74. Maior: Scharwenka 3,38, depois Rzewski 3,19, Lack 3,16, Scriabin 3,16, Fauré 2,91.
- Mais previsíveis depois de Victoria: C. L. Johnson 1,94, Raff 1,95, J. Scott 2,08, Nazareth 2,20, Joplin 2,20, Czerny 2,24. Bach 2,28, Scarlatti 2,25, Beethoven 2,25 e Handel 2,29 (Handel era 2,21 com as cópias).
- Compositor × nascimento: ρ = 0,50 (IC95% 0,24–0,74; p = 1,7e-4; n = 52).
- Por período (peças): Barroco 2,27 (3 compositores), Clássico 2,32 (4), Romântico 2,54 (33), Moderno 2,69 (11). Kruskal-Wallis H = 220, ε² = 0,10; permutando o período entre compositores, p = 0,008.
- O compositor explica η² = 0,37 da surpresa entre peças (nulo: média 0,024, p95 0,033).
- Confiabilidade: Spearman entre janela 1 e janela 2 = 0,71 dentro da peça; 0,97 entre médias por compositor.

**Veredito.** Não está na VALIDADE.md (a F8 veio depois). O REPORT da F8 trata o efeito de época como robusto ao nulo por compositor (p = 0,008), mas correlacional.

**O que NÃO se pode concluir.**
- Que perda baixa é "música simples" ou "esperada por Meyer": é previsibilidade para um modelo treinado no Lakh.
- Que a regularidade de tonalidade e ritmo explica a ordem: não foi medida com precisão (o controle por descritores simples está em Q6: 0,50 → 0,40). Compatível com ragtime e maxixe no extremo previsível, mas Raff e Victoria também estão lá, e os mais surpreendentes (Scharwenka, Lack, Rzewski) não formam um bloco estilístico óbvio.
- A tendência com a época pode refletir quanto cada repertório aparece no Lakh, o ruído da transcrição automática, o gênero e o tamanho do acervo (Renascimento tem 1 compositor, Barroco 3, Clássico 4).

## Q6. A cronologia do mapa se reduz à estatística de superfície? (F9, F10, F15)

**Resposta.** Sim, em parte. A cronologia continua depois de retirar descritores simples de superfície e o gênero do título, com queda de um quarto a um terço do ρ. O mapa feito só com os descritores acompanha a época bem menos que o do modelo.

**Números** (camada 6, média, 2 janelas; 52 compositores, 2.103 peças; 24 descritores simbólicos sem o modelo: notas por segundo, altura, duração, polifonia, intervalos, classes de altura).

| | Mantel ρ | R² do compositor | Sonda |
|---|---|---|---|
| Modelo (base) | 0,502 | 0,268 | 0,311 |
| Só descritores (sem o modelo) | 0,207 | 0,182 | 0,223 |
| Modelo sem descritores | 0,356 | 0,152 | 0,280 |
| Modelo sem gênero (título) | 0,374 | 0,194 | n/d |

- Os descritores explicam cerca de 50% (0,504) da variância das representações. RSA modelo × descritores = 0,650.
- Surpresa × época (compositor): 0,499 → 0,404 com os descritores controlados (p = 0,003); por peça, 0,329 → 0,210. Os descritores explicam 72% da surpresa.
- Gênero (regex do título; explica 8,3% da variância das peças): Spearman entre as matrizes de distância, base × resíduos, 0,91. O k = 2 deixa de isolar os sete pré-românticos (grupos de 25 e 27), mas os sete seguem no mesmo ramo.
- O que o eixo do tempo "ouve" (H17, F15): o PC1 do mapa acompanha sobretudo a polifonia média (ρ de Spearman entre compositores 0,85) e a duração média das notas (0,85), e menos o cromatismo, pela entropia de classes de altura (0,60); a extensão fica em 0,43. Polifonia e duração provavelmente são redundantes (notas longas empilham notas soando juntas). Leitura: para o modelo, "mais recente" é sobretudo mais notas soando juntas e sustentadas. É correlação, não mecanismo: gênero, instrumento e gravação se confundem com a época (n = 52). Figura de apoio: `analysis/F15_eixos/figs/eixos_descritores.png`.
- Nulo: 1.000 permutações dos nascimentos dão p95 ≈ 0,104. Todos os ρ ficam acima; Mantel p = 0,0002 é o mínimo possível e não distingue entre eles.

**Hipóteses (registradas antes, PLANO_V2).**
- **H8** (mapa só de descritores acompanha a época, menos que o modelo): 0,207 contra 0,502. Confirmada.
- **H9** (RSA < 0,7): 0,650. Confirmada, mas os dois mapas compartilham muito.
- **H10** (cronologia sobrevive, ρ > 0,3): 0,356. Confirmada, com queda; a sonda cai pouco (0,311 → 0,280), o R² do compositor cai mais.
- **H11** (surpresa × época cai, mas não some): 0,50 → 0,40. Confirmada.
- **H12** (cronologia sobrevive ao gênero, ρ > 0,3, e o bloco continua): 0,374 confirma a primeira parte; o bloco só na leitura fraca.
- **H17** (PC1 acompanha cromatismo, polifonia e extensão, com ρ > 0): 0,60, 0,85 e 0,43 entre compositores (p de permutação < 0,001, < 0,001 e 0,001). Confirmada nos sinais registrados; a polifonia e a duração dominam e o cromatismo é o mais fraco dos três (fora da VALIDADE).

**Veredito (VALIDADE, linhas 13–16).** H8/H9: **sobrevive**. H10: **sobrevive, com queda**. H11: **enfraquece**. H12: **sobrevive** para a cronologia; bloco pré-romântico **enfraquece**.

**O que NÃO se pode concluir.**
- Que a cronologia independe da superfície: os descritores levam cerca de 29% do ρ e 72% da surpresa. A queda de 0,502 para 0,356 não foi testada (sem nulo nem IC).
- Que o controle é completo: é linear e com descritores simples; superfície mais rica ou não linear poderia reduzir mais. As classes de altura não são transpostas, então o controle inclui tonalidade.
- Que o gênero foi removido: 52% das peças caem em "outro" no regex do título. Gênero e época se correlacionam (fuga é barroca), então a queda não separa "gênero confundindo" de "gênero como parte do estilo da época".
- Que o ρ restante é "conhecimento de história": pode ser gênero, instrumentação, gravação ou transcrição.
- Controle simultâneo de gênero e descritores não foi feito; bootstrap do k = 2 sob resíduos de gênero também não.

## Q7. Relações novas (F11–F13)

**Finais de obra (F12, H13).** *Base sem cópias (2.103 peças, `metrics.json` regerado; o REPORT da F12 ainda cita 2.183 peças e os números antigos).* Hipótese: o final fica mais perto do centróide do período que o início (mais "convencional"; a leitura de Meyer é nossa, sem atribuição específica). **Cai.**
- Δ distância ao centróide do período (final − início) = −0,0086, cerca de 1% da distância (52,8% das peças; Wilcoxon unilateral p = 0,0005). Ao centróide do compositor, −0,0061 (50,6% das peças; p = 0,012).
- Por compositor, o sinal é só marginal (34 de 52, p = 0,018 unilateral, para o período) ou nulo (28 de 52, p = 0,34, para o compositor). O sentido é oposto no Barroco e no Clássico (+0,021 e +0,033) e a favor no Romântico (−0,018) e no Moderno (−0,032).
- A perda média quase não muda (início 2,476; final 2,474), e a correlação entre Δ distância e Δ perda é −0,15: parte do efeito parece previsibilidade ou textura simples, não "convenção". Sem correção para comparações múltiplas; pseudo-replicação por peça. Veredito (linha 17): **cai**.

**Fio brasileiro e valsas (F13, H14, exploratório).** H14 (tangos e maxixes de Nazareth mais perto do ragtime que as valsas) não era testável pelo título (1 tango, 0 valsa). Os gêneros de 13 das 22 peças foram verificados em fontes externas (IMSLP, Musica Brasilis, Nazareth 150 anos, e uma fonte comercial para Rosa Maria).
- Nazareth, 4 valsas contra 8 tangos e polcas: distância ao ragtime 1,096 contra 0,546; a Chopin 0,417 contra 1,085. Mann-Whitney unilateral p = 0,002 (separação completa, o menor p possível; sem Rosa Maria, p = 0,006).
- Ragtime: as 4 peças com "waltz" no título (3 de Joplin, 1 de C. L. Johnson) contra 79 rags: a Chopin 0,824 contra 1,208 (p = 0,0003); ao ragtime 0,452 contra 0,216 (p = 0,0005). Na figura, o efeito não é uniforme: só duas das quatro ficam bem perto de Chopin.
- Descritivo (do `metrics.json` da F13, regerado com 2.103 peças; o REPORT ainda cita 0,354 e 0,579): Nazareth (22 peças) é o compositor mais próximo do centróide do ragtime entre os 49 fora do grupo (0,352; o 2º é Czerny, 0,535). Villa-Lobos fica longe (1,169; 46º de 49): não há fio de ragtime nele neste espaço. Tico-Tico: 0,437 ao ragtime e 1,410 a Chopin (valsas_metrics.json, base nova).
- **Leitura:** neste espaço, as valsas de Nazareth e do ragtime ficam mais perto de Chopin que os tangos, polcas e rags dos mesmos autores. Não é dizer que a valsa atravessa culturas: valsa é 3/4 e tango e rag são 2/4, e o modelo pode estar captando só o compasso. Ressalva: não se conclui que ele "reconhece" a valsa como categoria estilística; andamento lento, textura romântica e transcrição também não estão descartados. n muito pequeno; 9 títulos de Nazareth não verificados; valsas de ragtime identificadas só pela palavra "waltz". Veredito (linha 18): **sobrevive, exploratório**. O teste de compasso (F14, H15 refutada) indica que não parece ser só o 3/4: dentro do mesmo compositor, as valsas se agrupam entre si (9 de 10 compositores, p = 0,004), mas minuetos, mazurcas e polonaises não ficam mais perto delas do que as danças binárias (−0,009, p = 0,43). Com n pequeno (10 compositores); um sinal contrário fraco aparece só em minuetos, Ländler e sarabandes (5 de 5 compositores, p = 0,0625, o mínimo possível com n = 5).

**"À frente ou atrás do tempo" (F11), só como ilustração.** Resíduo do PC1 do mapa contra o ano de nascimento (PC1 explica 33,8%; Spearman 0,50; R² da reta 0,32), com IC95% por bootstrap de peças.
- 36 de 52 têm IC que exclui zero. Soam mais "modernos" que a data: 20 (Victoria 0,45, Scharwenka 0,40, Meyer-Helmund 0,39, Fauré, Balakirev, Scriabin, Debussy, Chopin...). Mais "antigos": 16 (Johnson −0,70, J. Scott −0,66, Joplin −0,44, Haydn −0,35, Beethoven −0,30, Mozart −0,28...). Handel e Rzewski deixaram a lista; Medtner e Rebikov entraram nos "modernos". O padrão: ragtime e clássicos abaixo da reta; romantismo médio e tardio acima.
- **Ressalva (decisão: só ilustração).** O IC mede só a amostragem das peças; não inclui a incerteza da reta nem da PCA, e não há nulo. Com R² de 0,32, um desvio de grupo (todo o Classicismo, o ragtime) gera resíduos "significativos" em bloco, então 36 de 52 não são 36 casos notáveis. Victoria (1548) tem alavancagem e extrapolação; Meyer-Helmund agora tem só 6 peças. É posição no espaço do modelo, não juízo histórico sobre inovação. Fora da VALIDADE.

**Mudança dentro da carreira (F17, H21 não confirmada).** Testamos se as obras tardias de um compositor ficam mais "à frente" no eixo do tempo do mapa, usando o número de opus como data aproximada. Não ficam: em 9 compositores, a média ponderada do ρ é 0,008 (5 de 9 positivos). Nem Scriabin, que vai de um estilo chopiniano a um quase atonal, mostra efeito (ρ = 0,05, p = 0,69). A exceção é Chopin (ρ = 0,44, p = 0,002). O eixo do tempo do modelo separa épocas, mas não acompanha a evolução individual. Ressalvas: o opus é um proxy de data e há poucas peças por compositor.

## Hipóteses

| Hipótese | Previsão | Resultado | Veredito |
|---|---|---|---|
| F2 | Camadas intermediárias ≥ última | Média: camada 6 = 0,311 contra camada 12 = 0,186; último token: 0,166 (camada 5) contra 0,057 (12). A 6 não se distingue da 5, 7, 8 e 9 (mantida pela regra de 0,02). | Confirma na direção; sem intervalo |
| H1 | Distância entre centróides cresce com a diferença de época | Mantel ρ = 0,502, p = 0,0002; 0,415–0,49 nas outras representações | Sobrevive; efeito moderado |
| H2 | Nacionalidade pesa menos e pode sumir ao controlar a época | ρ = 0,082 (p = 0,020); parcial 0,040 (p = 0,116) | Sobrevive, com cautela (sem evidência de efeito) |
| H3 | O compositor explica uma minoria da variância entre peças | R² = 0,268 (nulo 0,0243); 66,9% das peças mais perto de outro centróide | Sobrevive; o valor depende da representação (0,12–0,27) |
| H4 | O gênero rivaliza com o compositor | R² do gênero 0,155 contra 0,303 do compositor (1.000 peças) | Não se confirma; enfraquece |
| H5 | O espaço é um contínuo; o ramo destacado, se houver, é o Barroco | Razão 1,911 contra p95 do nulo 2,38; corte em 2 estável (ARI 0,787), bloco de 7 pré-românticos | Contínuo sobrevive; ramo é pré-romântico, não só Barroco; k ≥ 3 enfraquece, exploratório (ARI 0,68–0,73; regiões estáveis sem as cópias, razão da lacuna ainda dentro do nulo) |
| H6 | O vetor centrado desloca mais que o aleatório e que nenhum, de forma monótona em α | 0,684 contra 0,433 e 0,392 (α = 1); 7 de 7 sementes, p = 0,016; média sobe até α = 1,5 (0,755), mas só 4 de 7 trajetórias são monótonas | Sobrevive, como deslocamento parcial; em 3 de 4 direções interpretáveis (falha em Joplin → Chopin: 5/7, p = 0,69; Haydn → Mozart não interpretável) |
| H7 | O progresso Bach → Chopin é monótono; intermediários perto dos clássicos é pergunta aberta | t = 0 → 0,277; 0,5 → 0,338; 1 → 0,688 (monótono, não linear); Mozart e Beethoven são os clássicos mais próximos do segmento (geometria) | Enfraquece (só Bach ↔ Chopin; sem teste para "Bach domina") |
| H8 | O mapa só de descritores acompanha a época, menos que o do modelo | Mantel ρ = 0,207 contra 0,502 | Sobrevive |
| H9 | RSA modelo × descritores < 0,7 | 0,650; descritores explicam cerca de 50% da variância | Sobrevive |
| H10 | A cronologia sobrevive sem os descritores (ρ > 0,3) | 0,356 (p = 0,0002, piso); sonda 0,311 → 0,280 | Sobrevive, com queda (controle linear) |
| H11 | Surpresa × época cai com os descritores, mas não some | 0,499 → 0,404 (p = 0,003); por peça 0,329 → 0,210; descritores explicam 72% da surpresa | Enfraquece |
| H12 | A cronologia sobrevive ao gênero (ρ > 0,3); o bloco pré-romântico continua | 0,374 (p = 0,0002); bloco no mesmo ramo, mas o k = 2 deixa de isolá-lo (25 contra 27) | Cronologia sobrevive; bloco enfraquece |
| H13 | Os finais são mais convencionais que os inícios | Δ período −0,0086 (cerca de 1%; 52,8% das peças); por compositor 34/52 e 28/52; sinal oposto no Barroco e no Clássico | Cai |
| H14 | As valsas de Nazareth ficam longe do ragtime e perto de Chopin | 4 valsas contra 8 tangos e polcas: 1,096 contra 0,546 (ragtime), 0,417 contra 1,085 (Chopin); p = 0,002 (piso) | Sobrevive (exploratório, n muito pequeno) |
| H15 | Se o agrupamento da valsa fosse só compasso, as outras ternárias ficariam tão perto das valsas quanto as valsas entre si, e mais que as binárias (F14) | Dentro do compositor (n = 10): valsa–ternária contra valsa–binária −0,009 [−0,081; 0,081], p = 0,43; valsa–valsa contra valsa–ternária −0,088, 9 de 10 compositores, p = 0,004 | Refutada: as valsas se agrupam entre si, mas as outras ternárias não ficam mais perto delas que as binárias |
| H17 | O eixo do tempo (PC1) acompanha cromatismo, polifonia e extensão (ρ > 0) | ρ entre compositores: polifonia 0,85, duração 0,85, cromatismo 0,60, extensão 0,43 | Confirmada; polifonia e duração dominam, o cromatismo pesa menos |
| H18 | Entre os românticos, a mesma nacionalidade aproxima os centróides (Mantel parcial > 0) | ρ parcial = −0,01, p = 0,52 (33 compositores, 528 pares) | Não confirmada (poder baixo; ausência de evidência) |
| H19 | No steering Mozart → Debussy, os descritores vão na direção de Debussy (entropia, polifonia, duração) em mais de 4 de 7 sementes | Polifonia e duração 7/7 (p = 0,016); entropia de classes 1/7 e 4/7 (p ≥ 0,22) | Parcial |
| H20 | Controle de perfil oposto (Chopin → Joplin): se o efeito for do alvo, duração e polifonia caem e as notas/s sobem | Notas/s 15,3 → 18,5 (7/7 contra o aleatório, p = 0,016); duração 0,30 → 0,26 (p = 0,30); polifonia 3,56 → 4,24, sobe nos três pares | Mista: o andamento depende do alvo, a polifonia parece efeito comum |
| H21 | Dentro da carreira, o opus acompanha o eixo do tempo (F17) | 5 de 9 com ρ > 0; média ponderada de 0,008; Scriabin 0,05 (p = 0,69); só Chopin com efeito (0,44, p = 0,002) | Não confirmada |

## Leitura à luz de Meyer

Esta seção é interpretação. Usa a ideia geral de que o estilo se organiza em níveis (do dialeto de uma época até as escolhas dentro de uma obra) e de que expectativa e surpresa importam. Não atribuímos a Meyer afirmações específicas que não conferimos, e não há citações nem páginas. Só ligamos aos níveis os resultados que sobrevivem.

- **Dialeto, época (H1, H5):** a distância crescer com a diferença de nascimento (ρ = 0,502) e o bloco pré-romântico se separar de modo estável (ARI 0,787) são compatíveis com a ideia de que as épocas compartilham um dialeto. O fato de o espaço ser contínuo e o PC1 acompanhar a cronologia só em parte (ρ = 0,499) sugere que o dialeto muda gradualmente, sem fronteiras nítidas. Lembrar que há poucos barrocos e clássicos.
- **Idioma do compositor (H3):** o compositor explica uma minoria da variação (R² = 0,268, nulo 0,0243), e o acerto médio de 0,337 é muito acima do acaso. Isso sugere que há um idioma reconhecível por compositor, mas frouxo: a nuvem de cada um se sobrepõe à dos vizinhos. É uma leitura do modelo, que vê só notas e tempos.
- **Estilo interno da obra:** janelas da mesma peça são mais próximas entre si do que de outras peças do mesmo compositor (52 de 52). É compatível com a ideia de que cada obra tem uma coerência própria. Mas nossa medida mistura essa coerência com a gravação e o arquivo MIDI, e não mede as expectativas dentro da obra. Por isso fica como indício fraco.
- **Escolhas dentro de restrições (H6, H7):** somar o vetor de Chopin move a continuação no eixo (0,684 contra 0,392 sem steering; 7 de 7 sementes), mas a música não chega ao centróide dele (distância 0,930). Uma leitura possível, sem teste direto, é que o vetor médio captura uma parte da restrição de um estilo, e a música gerada ainda faz escolhas que o vetor não fixa. O vetor também desloca em Mozart → Debussy e Chopin → Bach, mas não em Joplin → Chopin. Nos descritores independentes, o andamento (duração e notas por segundo) depende do alvo, e a polifonia sobe nos três pares testados. O caminho Bach → Chopin só foi testado em Bach ↔ Chopin.
- **Convenções compartilhadas (F13, exploratório):** as valsas de dança ficam juntas no mapa apesar de os autores serem diferentes. Para o modelo, as valsas de Nazareth, Joplin e Johnson ficam mais perto de Chopin que dos tangos e rags de seus próprios autores (0,417 contra 1,085 em Nazareth; p = 0,002). Uma leitura possível é que o gênero funciona como uma convenção compartilhada acima do compositor, o que seria compatível com a ideia de estilo em níveis. Mas n é muito pequeno; o teste de compasso (F14) indica que não parece ser só o 3/4, sem excluí-lo; não se conclui que ele reconhece a valsa como categoria estilística. Finais de obra (H13) não deram suporte a uma leitura de "convenção" no nível da obra.
- **Expectativa (F8):** a surpresa do modelo cresce, em média, com a época (ρ = 0,50, IC95% 0,24–0,74), e os ragtimes e os barrocos estão entre os mais previsíveis. Não distinguimos entre repertório mais ou menos presente no Lakh e regularidade da própria música. Mas a expectativa aqui é a de um modelo treinado no Lakh, não a de um ouvinte, e a regularidade de tonalidade e ritmo não foi medida de forma própria. Com descritores simples controlados, a relação cai de 0,50 para 0,40, mas não some (Q6).

## O que o modelo não vê / limitações

- **Pedal, andamento e dinâmica.** No código do AMT instalado (`anticipation/convert.py`), as mensagens de controle, que incluem o pedal, são ignoradas ("ignore for now"). Os eventos usados na extração têm só três campos: tempo, duração e nota (`F0_infra/extract_amt.py`). Não há token de andamento: o tempo é medido em segundos reais, que vêm da execução transcrita. Marcações de dinâmica (velocity) não entram nesses eventos. O `use_tempos = false` e o `use_sustain_pedals = false` do PLANO.md e do `tokenizer_config.json` descrevem o tokenizador (miditok) do modelo original do repositório; o AMT usado nos resultados tem tokenização própria, e a leitura acima vem do código dele. A janela é limitada a 341 eventos e a 100 s.
- **Pianista e gravação.** O GiantMIDI transcreve gravações do YouTube. O intérprete se mistura com o compositor, e a transcrição automática adiciona ruído. Isso afeta sobretudo a coesão por obra e a surpresa.
- **Modelo.** O AMT foi treinado no Lakh MIDI, não em música clássica. "Perto" e "surpreendente" são relativos a esse treino.
- **Amostra.** Poucos compositores barrocos (3), clássicos (4) e do Renascimento (1). Só 52 compositores.
- **Metadados.** Nascimento e nacionalidade foram curados à mão e não verificados em fonte externa. A verificação por web foi bloqueada no ambiente.
- **Base de dados.** A base tem 2.103 peças depois de remover 80 cópias (37 grupos de MIDIs idênticos byte a byte, a mesma gravação sob títulos diferentes; ver "Base de dados"). As conclusões não mudaram. F6 (transposição) e F7 (steering) são da base anterior, (a F12 e a parte descritiva da F13 foram regeradas com a base nova). Outras duplicatas parciais (vetores quase idênticos) podem existir. Meyer-Helmund ficou com 6 peças.
- **Mapa 2D.** Distorce as distâncias (Spearman 0,75). Serve para ilustrar; as medidas são feitas no espaço original.
- **Escolha de representação.** Camada, pooling e número de janelas mudam parte dos números (o R² do compositor vai de 0,12 a 0,27). A camada foi escolhida e avaliada nos mesmos dados.
- **Steering.** Quatro pares interpretáveis, sete sementes cada (no principal, sementes de Bach, uma peça por semente), sem escuta; os descritores independentes, só em três pares. O progresso é uma projeção num eixo.
- **Controles que faltam.** Andamento e dinâmica. A linha de base simbólica foi feita (F9), mas é linear e simples; controle conjunto de gênero e descritores não foi feito. Também faltam IC e nulo para vários números (F2, transposição, vizinhos).
- **Nomes.** Várias listas usam só o sobrenome; "Scott" pode ser J. Scott ou C. Scott.
- **Estabilidade (teste com 3 janelas por peça; fonte: `analysis/F6_controles/metrics_3janelas.json`; base anterior, com as cópias).** O núcleo pré-romântico se mantém, mas o bloco do corte em k = 2 ganha Mendelssohn e Victoria (9 compositores, ARI 0,753, razão de lacuna 1,732 contra p95 2,372). Fora isso, os resultados mudam pouco: camada 6 média com acurácia balanceada 0,368; Mantel ρ = 0,506 (p = 0,0002); nacionalidade parcial ρ = 0,041 (p = 0,114); R² do compositor 0,299 (63,9% das peças mais perto de outro centróide); H4: R² do gênero 0,179 contra 0,337. A base principal continua sendo 2 janelas.

## Figuras candidatas para a apresentação

Todas foram abertas e conferidas.

1. `analysis/F3_geometria/figs/mapa_apresentacao.png`. O mapa dos 52 compositores: Bach, Handel e Scarlatti ficam embaixo à esquerda, ragtime em cima à esquerda e os românticos e modernos para a direita. Mensagem: o eixo principal acompanha, em parte, a cronologia (distorção 0,75). O PC1 está invertido para o tempo crescer para a direita. Distingue J. Scott de C. Scott. É a figura mais forte para abrir.
2. `analysis/F3_geometria/figs/dist_vs_epoca.png`. Dispersão de cada par de compositores. Mensagem: a distância cresce com a diferença de época (Mantel ρ = 0,50, p = 0,0002), mas a nuvem é larga. Para além de cerca de 200 anos a distância deixa de crescer (e parece cair), e os poucos pares envolvem Victoria. Usar como figura de apoio.
3. `analysis/F5_topologia/figs/dendrograma.png`. Dendrograma dos centróides. Mensagem: o bloco Bach–Handel–Mozart–Haydn–Scarlatti–Beethoven–Hummel se separa cedo, e o resto vai se juntando de forma gradual (ARI do corte em 2: 0,787). Distingue J. Scott de C. Scott. Os cortes finos (k ≥ 3) são exploratórios: estáveis sem as cópias, mas não previstos; comentar como regiões, não ilhas.
4. `analysis/F5_topologia/figs/h0_barras.png`. Barras de fusão contra o nulo gaussiano de 90%. Mensagem: a maior fusão (0,553) fica dentro da faixa do nulo, ou seja, não há lacuna fora do que uma nuvem sem grupos produz (razão 1,911, p95 do nulo 2,38). Na figura, a maior parte da curva fica abaixo da faixa (fusões mais curtas que as de gaussianas): não ler como "curva dentro da faixa".
5. `analysis/F4_nuvens/figs/dispersao.png`. Dispersão intra-compositor com n = 20. Mensagem: ragtime, Meyer-Helmund e Victoria são compactos; Heller, Ravina e Gurlitt são espalhados. J. Scott (0,297) e C. Scott (0,667) aparecem como barras separadas. A compacidade pode vir do arquivo MIDI, e Meyer-Helmund tem só 6 peças.
6. `analysis/F2_representacao/figs/camadas.png`. Acurácia por camada. Mensagem: as camadas do meio separam melhor os compositores do que a última (0,31 na camada 6; 0,19 na 12; acaso 0,019); o último token é pior que a média. Os rótulos usam ponto decimal (0.31). Sem intervalo de confiança.
7. `analysis/F7_deslocamento/figs/steering_alfa.png`. Varredura de α. Mensagem: quanto mais forte o vetor de Chopin, mais a continuação avança no eixo Bach → Chopin (0,38 a 0,75), e o vetor aleatório fica plano (0,38 a 0,47). O subtítulo diz "Repetição de trigramas não aumenta até α = 1,5", o que não garante música coerente. Por semente, só 4 de 7 são monótonas.
8. `analysis/F7_deslocamento/figs/steering.png`. Progresso por condição, α = 1, n = 14. Mensagem: o vetor centrado (0,68) fica bem acima do aleatório (0,43) e de nenhum (0,39), e o vetor de Bach sozinho piora (0,28). O título ("empurra a música gerada na direção de Chopin, sem chegar lá") já traz a ressalva: a música não chega ao alvo (a linha tracejada em 1,0). As colunas "caminho" repetem o centrado (t = 1) e levam à leitura "Bach domina", não testada.
9. `analysis/F7_deslocamento/figs/steering_dois_sentidos.png`. Bach → Chopin e Chopin → Bach. Mensagem: o efeito aparece nos dois sentidos (o título da figura diz "mais de Bach para Chopin", que é descritivo) (0,68 contra 0,39 e 0,43; 0,46 contra 0,33 e 0,29), menor no inverso. A comparação mistura eixos, sementes e n (14 contra 7); mostrar sem atribuir a assimetria ao vetor.
10. `analysis/F7_deslocamento/figs/steering_pares.png`. Progresso por condição nos 4 pares interpretáveis (média por semente ± erro padrão, 7 sementes). Mensagem: o vetor centrado fica acima do aleatório e de nenhum em Bach → Chopin (0,68), Chopin → Bach (0,46) e Mozart → Debussy (0,50), mas não em Joplin → Chopin (0,54 contra 0,49 e 0,44; 5 de 7, p = 0,69). Haydn → Mozart fica de fora (centróides a 0,10; não interpretável), citado na nota de rodapé. Figura de apoio ao slide 8 da apresentação.
11. `analysis/F8_expectativa/figs/surpresa_por_compositor.png`. Surpresa do modelo por compositor, em ordem de nascimento. Mensagem: Victoria, barrocos e ragtime ficam à esquerda da média (2,49), e Scharwenka, Rzewski, Lack e Scriabin ficam bem à direita; a tendência com a época é moderada (ρ = 0,50, IC95% 0,24–0,74). É surpresa para este modelo. Os IC variam bastante entre compositores.
12. `analysis/F9_superficie/figs/controles_cronologia.png`. Barras do Mantel ρ por controle: modelo (base) 0,502; sem gênero 0,374; sem estatísticas de superfície 0,356; só estatísticas de superfície, sem o modelo, 0,207; linha tracejada no p95 do nulo (≈ 0,104). Mensagem: a cronologia sobrevive aos controles e a superfície sozinha acompanha a época bem menos. Ressalva: o nulo foi calculado no espaço do modelo (referência de ordem de grandeza para a barra cinza) e as quedas não foram testadas. Para o slide "O mapa não é só estatística simples".
13. `analysis/F13_brasil/figs/valsas.png`. Dispersão: distância ao ragtime (x) × distância a Chopin (y), por peça. As 4 valsas de Nazareth ficam embaixo à direita (longe do ragtime, perto de Chopin), os tangos e polcas em laranja no centro e no alto, os 79 rags em cinza no canto superior esquerdo e a estrela do Tico-Tico no alto. As 4 valsas de ragtime (losangos) ficam espalhadas: Binks' e Wedding of the Fairies bem mais perto de Chopin, Augustan Club e Harmony Club não. Ressalva: o título da figura cita Joplin, mas uma das valsas de ragtime é de C. L. Johnson; exploratório, n pequeno, rótulo de Rosa Maria de fonte comercial.
14. `analysis/F4_nuvens/figs/nuvens_pecas.png`. As 2.103 peças em cinza e as nuvens de Bach (n = 129), Mozart (70), Chopin (96) e Joplin (31), com elipse de 1 desvio-padrão e centróide. Mensagem: Bach e Mozart se sobrepõem bastante; Chopin e Joplin ficam isolados; o subtítulo traz 27% de variação explicada (nulo 2%) e 67% das peças mais perto de outro centróide. Ressalva da própria figura: a projeção 2D distorce as distâncias, então a sobreposição visual não mede a do espaço original.
15. `analysis/F11_tempo/figs/tempo_vs_mapa.png`. Ano de nascimento × PC1, com reta tracejada, cor por período, barras de IC e contorno preto (asterisco) nos 36 compositores com IC do resíduo fora de zero. Mensagem: o eixo segue a cronologia (Spearman 0,50), mas o ragtime (Joplin, J. Scott, Johnson) e os clássicos ficam abaixo da reta e o romantismo médio e tardio, acima. Só como ilustração (ver Q7). Limitações visuais: rótulos de Meyer-Helmund e Scriabin se sobrepõem no alto e Victoria está isolada em 1548 (alavancagem).
16. `analysis/F15_eixos/figs/eixos_descritores.png`. Barras de Spearman do PC1 (eixo cronológico) e do PC2 com 10 descritores, por peça (n = 2.103) e por compositor (n = 52). Mensagem: o PC1 acompanha sobretudo polifonia (0,85) e duração média (0,85), e menos o cromatismo (0,60); o título da figura diz isso. Apoio ao slide 4. Ressalvas: correlação, não mecanismo; o sinal do PC2 é arbitrário; o IOI mediano e a fração de acordes são aproximações.
17. `analysis/F7_deslocamento/figs/descritores_tres_pares.png`. Centrado − nenhum (média ± erro padrão entre 7 sementes) para duração média e notas por segundo em Bach → Chopin, Mozart → Debussy e Chopin → Joplin, com a direção esperada do alvo (triângulos). Mensagem: a duração sobe em dois pares e não em Joplin; as notas/s caem em dois e sobem só em Joplin. Apoio ao slide 8. Ressalvas: não mostra polifonia nem entropia; 7 sementes; sem correção para comparações.

**Explorador interativo** (mapa dos 52 compositores com cor por período, nacionalidade ou surpresa; vizinhos, nuvens de peças, Tico-Tico e as setas do steering): https://claude.ai/artifact/NeP4zc74AncnZsXsZuLvvo. Material para quem quiser explorar; vale as mesmas ressalvas do mapa 2D.

Não recomendada: `analysis/F3_geometria/figs/mapa_pca.png` é a versão de trabalho do mapa. Tem rótulos sobrepostos e dois "Scott" sem distinção; usar a de apresentação.
