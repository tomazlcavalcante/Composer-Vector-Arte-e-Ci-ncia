# F7 — Deslocamento (Q4)

## Pergunta
Somar o vetor de um compositor move a música na direção esperada? O que há entre Bach e Chopin?

## Hipótese registrada
- **H6:** o vetor centrado desloca a música relida em direção ao alvo mais que um vetor aleatório e mais que a continuação sem steering, de forma monótona em α até a quebra.
- **H7:** no caminho Bach → Chopin a posição relida avança de forma monótona. Se os pontos intermediários caem perto dos clássicos é uma pergunta aberta.

## Configuração
- Camada 6, pooling média. Um único par: Bach → Chopin.
- **Bases mistas (importante):** o caminho geométrico (a) e `steering_forte.csv` (principal) usam os centróides da passada 1 (1 janela por peça; DIARIO, 2026-11-08, registra a direção Bach → Chopin como quase inalterada). A varredura de α e o par inverso Chopin → Bach usam centróides de 2 janelas. Os números de (a) (inclusive 0,880, 0,942 e a ρ = 0,53 de t × nascimento) são os da passada 1. Comparações entre seções misturam bases.
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
- A repetição média de trigramas ficou entre 1,5% e 4,1% nas condições do forte (a de "nenhum" é 4,14%, acima de 4%). Por continuação, o máximo é 28,9% no forte, 23,7% na varredura e 39,5% no inverso. Isso não exclui outros defeitos na música gerada.
- (a): ρ = 0,53 entre t e nascimento é moderado. Scriabin (t = 1,08) e Debussy (t = 1,02) projetam além de Chopin. Não há nulo para a distância ao segmento.

## Varredura de α (rodada autônoma 1; `steering_alfa.csv`)
Bach → Chopin, camada 6, 7 sementes × 1 amostra por α, vetor centrado e aleatório com α em {0,25; 0,5; 1; 1,5}; "nenhum" (α = 0) como ponto comum. Progresso médio ± erro padrão (n = 7), calculado do CSV:

| α | centrado | aleatório |
|---|---|---|
| 0 (nenhum) | 0,382 ± 0,061 | 0,382 ± 0,061 |
| 0,25 | 0,474 ± 0,045 | 0,394 ± 0,050 |
| 0,5 | 0,585 ± 0,043 | 0,384 ± 0,045 |
| 1 | 0,682 ± 0,030 | 0,465 ± 0,066 |
| 1,5 | 0,755 ± 0,027 | 0,428 ± 0,033 |

- **H6 apoiada com 7 sementes** (no eixo e no modelo usados). A média do centrado sobe a cada α (por semente, a trajetória é monótona em apenas 4 de 7); a do aleatório fica entre 0,38 e 0,47, sem tendência. Centrado > aleatório em 5 de 7 sementes em α = 0,25 (Wilcoxon p = 0,078), 7 de 7 em α = 0,5 (p = 0,016), 6 de 7 em α = 1 (p = 0,031) e 7 de 7 em α = 1,5 (p = 0,016). Centrado > nenhum em 6, 7, 7 e 7 de 7 sementes.
- **Sem aumento sistemático da repetição de trigramas até α = 1,5** (isso não garante que a música seja coerente; é a única medida de degeneração usada). Repetição média de trigramas: centrado 0,034; 0,008; 0,023; 0,030 (α crescente); aleatório 0,015; 0,004; 0,026; 0,064; nenhum 0,038. A média global é 0,027. O valor máximo de uma continuação é 0,237 (centrado α = 0,25 e aleatório α = 1,5); não aparece trecho degenerado sistemático nas médias.
- Distância cosseno média ao centróide de Chopin: 1,178 (nenhum) → 0,849 (centrado, α = 1,5); aleatório 1,115–1,184. A distância a Bach sobe de 0,758 para 1,074.
- Ressalvas: a monotonia vale para a média; por semente, só 4 de 7 têm progresso não decrescente de α = 0,25 a 1,5. Uma amostra por semente e por α; a quebra pode estar além de 1,5, que foi o maior α testado. Esta varredura usou centróides de 2 janelas por peça; `steering_forte.csv` usou os de 1 janela, o que muda um pouco o eixo, então os valores em α = 1 não são idênticos (0,682 contra 0,684 do forte, com amostras e eixo diferentes). Progresso é projeção num eixo, não "chegar a Chopin" (0,755 é o máximo, e a distância ao alvo segue em 0,85).

## Par inverso Chopin → Bach (`steering_forte_Chopin_Bach.csv`)
Mesmas condições de `steering_forte.csv`, origem Chopin e alvo Bach, α = 1, 7 sementes × 1 amostra (n = 7 por condição). Progresso: 0 = centróide de Chopin, 1 = centróide de Bach.

| condição | Bach → Chopin (n = 14; centróides de 1 janela) | Chopin → Bach (n = 7; centróides de 2 janelas) |
|---|---|---|
| nenhum | 0,392 ± 0,034 | 0,325 ± 0,037 |
| aleatório | 0,433 ± 0,038 | 0,287 ± 0,038 |
| centrado | 0,684 ± 0,024 | 0,461 ± 0,035 |
| caminho t = 0 | 0,277 ± 0,016 | 0,188 ± 0,026 |
| caminho t = 0,5 | 0,338 ± 0,026 | 0,408 ± 0,024 |
| caminho t = 1 | 0,688 ± 0,022 | 0,440 ± 0,030 |

- **Efeito nos dois sentidos.** Por semente (7), centrado > aleatório e centrado > nenhum em 7 de 7 (Wilcoxon p = 0,016) em ambos. Aleatório não supera "nenhum" no inverso (0,287 contra 0,325).
- **Assimetria.** Ganho do centrado sobre "nenhum": +0,292 de Bach para Chopin, +0,136 de Chopin para Bach (sobre aleatório: +0,251 e +0,174). Distância ao alvo com o centrado: 0,930 (centróide de Chopin) contra 0,896 (centróide de Bach). No sentido inverso o ganho foi menor, mas a comparação mistura eixos, sementes, bases de centróides (1 janela no forte, 2 no inverso) e n (14 contra 7): é uma observação descritiva, sem teste, e não permite atribuir a diferença ao vetor.
- **Mistura meio a meio.** Em cada sentido, t = 0 é o vetor da origem e t = 1 o do alvo. No sentido Bach → Chopin, o ponto médio (0,338) fica a 15% do caminho entre t = 0 (0,277) e t = 1 (0,688), isto é, junto ao vetor de Bach (a origem). No inverso, o ponto médio (0,408) fica a 87% do caminho entre t = 0 (0,188) e t = 1 (0,440), isto é, junto ao vetor de Bach (agora o alvo). Nos dois sentidos a mistura fica mais perto do vetor de Bach que do de Chopin. Isto é descritivo, sem teste: "Bach domina a mistura" é uma leitura causal não apoiada com um par e 7 sementes. A norma não é confundidor (todo vetor é renormalizado), mas t = 0,5 muda a direção, e a diferença entre t = 0,5 (0,338) e "nenhum" (0,392) é menor que 2 erros padrão.
- Ressalvas: o inverso tem n = 7 (uma amostra por semente), contra 14 do forte; a comparação de assimetria é entre eixos diferentes (origem e alvo trocados, e o inverso é medido a partir de sementes de Chopin), então parte da diferença pode vir do eixo e das sementes, não só do vetor. Repetição de trigramas mais alta no inverso em "nenhum" (0,124) e "aleatório" (0,120), contra 0,019–0,049 nas demais condições (no forte, "nenhum" tem 0,041); as continuações sem steering de Chopin são mais repetitivas, o que pode afetar o progresso medido. t = 1 e "centrado" são o mesmo vetor (0,440 contra 0,461, ruído da geração).

## Figuras
- [Progresso por condição de steering](figs/steering.png)
- [Varredura de α](figs/steering_alfa.png)
- [Dois sentidos, Bach → Chopin e Chopin → Bach](figs/steering_dois_sentidos.png)

## Ideias fora do escopo
- Grade completa de steering: outros pares, α > 1, mais sementes.
- Outros eixos de medida (distância ao centróide em vez de projeção).
- Avaliação auditiva do que é gerado (fora do escopo do ensaio).
- Mais pontos no caminho (t = 0,25; 0,75).

## Descritores independentes (`descritores.py`; `descritores_ref.csv`, `descritores_steering.csv`, `metrics_descritores.json`)
Descritores simbólicos calculados direto dos tokens (sem o modelo): notas/s (notas ÷ intervalo do primeiro ataque ao último fim), altura MIDI média e desvio, extensão (p95 − p5), duração média (s) e polifonia média (grade de 50 ms). Referência: janela do meio (341 eventos) de 129 peças de Bach e 96 de Chopin (média ± desvio entre peças). Steering: mesma geração de `steering_forte` (camada 6, α = 1, 7 sementes de Bach × 2 amostras, 120 tokens novos = 40 notas), descritores só da continuação; diferenças pareadas por semente (média das 2 amostras). "Direção de Chopin" = sinal de média_Chopin − média_Bach na referência (todas positivas aqui). Sementes na direção de Chopin e p (Wilcoxon) para centrado − nenhum / centrado − aleatório:

| descritor | Bach | Chopin | nenhum | aleatório | centrado | sementes na direção (vs nenhum; vs aleatório) | p (vs nenhum; vs aleatório) |
|---|---|---|---|---|---|---|---|
| notas por s | 7,95 ± 2,98 | 9,34 ± 4,14 | 9,04 | 9,34 | 4,84 | 0/7; 0/7 | 0,016; 0,016 |
| altura média | 63,3 ± 2,4 | 63,8 ± 4,1 | 63,6 | 64,5 | 60,7 | 1/7; 1/7 | 0,031; 0,031 |
| desvio da altura | 10,2 ± 1,6 | 11,5 ± 2,0 | 8,90 | 7,68 | 9,52 | 5/7; 7/7 | 0,22; 0,016 |
| extensão p95−p5 | 31,8 ± 4,5 | 36,8 ± 6,6 | 26,4 | 23,4 | 28,8 | 4/7; 6/7 | 0,22; 0,031 |
| duração média (s) | 0,37 ± 0,23 | 0,63 ± 0,34 | 0,30 | 0,28 | 0,65 | 7/7; 7/7 | 0,016; 0,016 |
| polifonia média | 2,44 ± 0,82 | 4,80 ± 1,47 | 2,38 | 2,35 | 2,95 | 6/7; 7/7 | 0,078; 0,016 |

Interpretação (cautelosa):
- **A lentidão dos exemplos MIDI é sistemática neste conjunto**: notas por segundo cai em 7 de 7 sementes (4,8 contra 9,0 sem steering). Mas isso é contra a referência: Chopin tem *mais* notas/s que Bach (9,3 contra 8,0, com dispersão grande), então a queda é *oposta* à direção da referência e não é "efeito Chopin" no sentido simbólico. A duração média das notas sobe para 0,65 s (Chopin de referência: 0,63 s; Bach: 0,37 s), em 7 de 7, e a polifonia sobe um pouco (2,95 contra 2,4; Chopin 4,8). Leitura plausível: o vetor produz notas longas e sustentadas, espaçadas, o que reduz notas/s e se aproxima de Chopin só em duração e (parcialmente) polifonia.
- Altura média desloca para baixo (60,7), contra a referência (diferença Bach–Chopin é pequena, 0,5 semitom). Desvio e extensão da altura sobem em relação ao aleatório (7/7, 6/7), mas não de forma distinguível de "nenhum" (p = 0,22); os dois controles (nenhum, aleatório) têm valores abaixo da referência de Bach, ou seja, a continuação gerada é mais estreita que a janela real em qualquer condição.
- Convergência parcial, então: duração e polifonia (e, contra o aleatório, dispersão de altura) acompanham a direção de Chopin; notas/s e altura média não.
- Ressalvas: n = 7 sementes (p mínimo 0,016), um só par e uma só camada/α; as 2 amostras por semente não são independentes; descritores simples, que não capturam harmonia ou textura; a referência é uma janela de 341 eventos, a continuação tem só 40 notas (descritores mais ruidosos, e notas/s e polifonia dependem do intervalo medido); a polifonia pode subir só porque durações maiores sobrepõem mais, e o aumento de duração e a queda de notas/s são um mesmo fenômeno de andamento; sem controle de comprimento do trecho; sem verificação auditiva.

## Outros pares (rodada contínua, 08/11)

**Outros pares** (`analysis/F7_deslocamento/pares_resumo.csv`; 7 sementes, 1 amostra por condição, α = 1, centróides de 2 janelas, exceto Bach → Chopin, que usa a base "forte" de 1 janela):

| Par | Distância entre centróides | Nenhum | Aleatório | Centrado | Centrado > aleatório |
|---|---|---|---|---|---|
| Bach → Chopin | 1,60 | 0,39 | 0,43 | 0,68 | 7/7 (p = 0,016) |
| Chopin → Bach | 1,60 | 0,33 | 0,29 | 0,46 | 7/7 (p = 0,016) |
| Mozart → Debussy | 1,71 | 0,23 | 0,28 | 0,50 | 6/7 (p = 0,031) |
| Joplin → Chopin | 1,11 | 0,44 | 0,49 | 0,55 | 5/7 (p = 0,69) |
| Haydn → Mozart | 0,10 | — | — | — | não interpretável |

O efeito se repete em 3 das 4 direções interpretáveis e falha em Joplin → Chopin. Haydn e Mozart estão quase sobrepostos no mapa (distância de 0,10), então o eixo "origem → alvo" não está bem definido e o progresso sai do intervalo 0–1. **Leitura:** H6 deixa de depender de um par só, mas não vale para qualquer par. Nos três pares em que funcionou, os compositores estão distantes no mapa (distância ≥ 1,6). Com 4 pares, a relação entre distância e efeito é só sugestiva.

## Descritores em Mozart → Debussy (H19; `descritores.py --src "Mozart, Wolfgang Amadeus" --tgt "Debussy, Claude"`; `*_Mozart_Debussy.*`)
Mesmo procedimento da seção anterior (camada 6, α = 1, 7 sementes de Mozart × 2 amostras, 120 tokens novos, descritores só da continuação, 2 janelas por peça nos centróides). Referência: janela do meio de todas as peças de Mozart e de Debussy. Foi acrescentada a entropia de classes de altura (bits, máx. 3,58), só nos pares novos; o padrão Bach → Chopin continua com 6 descritores. "Direção de Debussy" = sinal de média_Debussy − média_Mozart. Sementes na direção (vs nenhum; vs aleatório) e p de Wilcoxon (centrado − nenhum; centrado − aleatório):

| descritor | Mozart | Debussy | nenhum | aleatório | centrado | sementes na direção de Debussy | p |
|---|---|---|---|---|---|---|---|
| entropia de classes | 3,05 ± 0,21 | 3,15 ± 0,26 | 2,76 | 2,58 | 2,66 | 1/7; 4/7 | 0,22; 0,81 |
| polifonia média | 2,75 ± 1,03 | 6,90 ± 2,46 | 2,37 | 2,30 | 4,59 | 7/7; 7/7 | 0,016; 0,016 |
| duração média (s) | 0,38 ± 0,22 | 0,95 ± 0,49 | 0,29 | 0,28 | 1,05 | 7/7; 7/7 | 0,016; 0,016 |
| notas por s | 8,14 ± 2,98 | 8,90 ± 4,69 | 9,52 | 10,33 | 7,04 | 1/7; 1/7 | 0,16; 0,031 |
| altura média | 65,5 ± 3,5 | 64,9 ± 5,1 | 65,7 | 66,1 | 63,8 | 4/7 (direção -); 5/7 | 0,47; 0,11 |
| desvio da altura | 10,5 ± 2,1 | 12,1 ± 2,5 | 10,3 | 9,6 | 13,9 | 7/7; 7/7 | 0,016; 0,016 |
| extensão p95−p5 | 33,6 ± 7,1 | 39,6 ± 9,3 | 31,8 | 30,2 | 45,7 | 7/7; 7/7 | 0,016; 0,016 |

- **H19 parcialmente apoiada.** Dos três descritores nomeados, polifonia e duração vão na direção de Debussy em 7/7 sementes contra os dois controles. A entropia de classes de altura **não**: 1/7 contra nenhum e 4/7 contra aleatório (p ≥ 0,22), e o centrado (2,66) fica abaixo do nenhum (2,76).
- **Genérico × específico.** O padrão se parece muito com o de Bach → Chopin: notas bem mais longas (0,29 → 1,05 s; Bach → Chopin 0,30 → 0,65), mais sobrepostas (2,4 → 4,6; antes 2,4 → 3,0), menos notas por segundo (9,5 → 7,0, contra a direção da referência, como antes) e altura média mais baixa (65,7 → 63,8; antes 63,6 → 60,7). Os mesmos descritores mudam do mesmo jeito em dois alvos diferentes, o que é o que se espera de um efeito genérico do steering ("notas longas, sustentadas, espaçadas"). A direção de Debussy coincide com essa mudança em duração e polifonia só porque Debussy também tem notas longas e muito sobrepostas; o que seria específico do alvo, a entropia de classes (cromatismo), não se move. A diferença que sobra é de intensidade (duração e polifonia sobem mais aqui, e Debussy tem valores de referência maiores) e a dispersão/extensão de altura, que aqui sobem em 7/7 contra o nenhum e o aleatório (antes, só contra o aleatório). Leitura: **mais genérico que específico**; compatível com Debussy em duração e polifonia, mas sem evidência de que o conteúdo harmônico do alvo seja transportado.
- Ressalvas: o argumento depende de comparar dois pares; sem um alvo de controle com perfil oposto (notas curtas e pouco sobrepostas, p. ex. um barroco ou ragtime) não dá para separar efeito genérico de efeito do alvo. Mesmas limitações da seção anterior (n = 7, amostras não independentes, continuação de 40 notas, polifonia e notas/s ligadas à duração, sem escuta). A referência usa `list_pieces` sem a remoção de duplicatas, o que não afeta este experimento. A referência de Mozart/Debussy tem diferenças de entropia pequenas (3,05 contra 3,15), então o teste de entropia tem pouca margem em qualquer caso.

## Controle de perfil oposto (Chopin → Joplin)

**H20 (registrada antes dos resultados, 08/11).** O efeito do steering sobre os descritores é específico do alvo ou genérico? Em Bach → Chopin e Mozart → Debussy o vetor centrado deixou as notas mais longas e mais sobrepostas e reduziu as notas/s, mas os dois alvos têm notas longas e sobrepostas. Controle: src = "Chopin, Frédéric", tgt = "Joplin, Scott" (ragtime: notas curtas, menos polifonia, mais notas/s; a confirmar na referência). Procedimento: `CV_WINDOWS=1,2 python3 descritores.py --src "Chopin, Frédéric" --tgt "Joplin, Scott"` (7 sementes, 2 amostras, nenhum / aleatório α = 1 / centrado α = 1, camada 6, 120 tokens novos; saídas `*_Chopin_Joplin.*`).
- Se **específico**: com o vetor de Joplin, duração média e polifonia caem e notas/s sobe, em relação a "nenhum" e a "aleatório".
- Se **genérico**: duração e polifonia sobem mesmo assim.

**Resultado** (`descritores_ref_Chopin_Joplin.csv`, `descritores_steering_Chopin_Joplin.csv`, `metrics_descritores_Chopin_Joplin.json`; execução de 3 min, 7 sementes × 2 amostras). A referência confirma o perfil oposto: Joplin tem notas mais curtas (0,33 s contra 0,63 s de Chopin), menos polifonia (3,9 contra 4,8) e mais notas/s (12,5 contra 9,3). "Direção de Joplin" = sinal de média_Joplin − média_Chopin. Sementes na direção (vs nenhum; vs aleatório) e p de Wilcoxon (centrado − nenhum; centrado − aleatório):

| descritor | Chopin | Joplin | nenhum | aleatório | centrado | direção de Joplin | sementes na direção | p |
|---|---|---|---|---|---|---|---|---|
| duração média (s) | 0,63 ± 0,34 | 0,33 ± 0,13 | 0,30 | 0,35 | 0,26 | − | 4/7; 6/7 | 0,30; 0,078 |
| polifonia média | 4,80 ± 1,47 | 3,92 ± 0,87 | 3,56 | 3,76 | 4,24 | − | 2/7; 2/7 | 0,078; 0,47 |
| notas por s | 9,34 ± 4,14 | 12,53 ± 2,74 | 15,33 | 13,03 | 18,48 | + | 5/7; 7/7 | 0,078; 0,016 |
| altura média | 63,8 ± 4,1 | 64,4 ± 2,3 | 64,4 | 64,1 | 65,9 | + | 5/7; 6/7 | 0,078; 0,031 |
| desvio da altura | 11,5 ± 2,0 | 12,9 ± 1,7 | 9,94 | 9,76 | 10,9 | + | 5/7; 7/7 | 0,078; 0,016 |
| extensão p95−p5 | 36,8 ± 6,6 | 41,4 ± 5,7 | 29,95 | 29,6 | 33,1 | + | 6/7; 6/7 | 0,11; 0,078 |
| entropia de classes | 3,10 ± 0,21 | 3,11 ± 0,11 | 2,23 | 2,55 | 2,49 | + | 5/7; 2/7 | 0,11; 0,58 |

**Veredito de H20: misto, sem apoiar claramente nenhuma das duas previsões.**
- **Duração:** a previsão "específica" se cumpre só em parte. A duração não sobe mais (0,30 → 0,26 s, diferença de −0,04 s, 4/7 sementes, p = 0,30 contra "nenhum"), ao contrário dos pares anteriores (+0,35 e +0,77 s). Contra o aleatório ela cai em 6/7 (p = 0,078), mas o aleatório está acima do "nenhum" (0,35), então esse contraste é frágil. Dizer que "a duração cai" seria exagero: o que se pode dizer é que o aumento desapareceu.
- **Notas por segundo:** sobem (15,3 → 18,5; 5/7 contra nenhum, p = 0,078; 7/7 contra aleatório, p = 0,016), o oposto dos dois pares anteriores (−4,2 e −2,5) e na direção de Joplin. É o indício mais claro de efeito dependente do alvo.
- **Polifonia:** sobe (3,56 → 4,24), só 2/7 sementes na direção de Joplin, ou seja, contra o alvo, e de magnitude parecida com a de Bach → Chopin (+0,57). Aqui a previsão "genérica" se cumpre. Como a duração não mudou, não dá para atribuir a polifonia à duração, ao contrário da ressalva anterior; fica sem explicação com estes descritores.
- Altura média, desvio e extensão sobem na direção de Joplin (5–7 sementes, p entre 0,016 e 0,11); a entropia de classes não distingue nada (2/7 contra aleatório).
- **Conclusão de conjunto (3 pares):** o efeito "notas longas, sobrepostas, poucas notas/s" não é um efeito fixo do vetor centrado: duração e notas/s mudam de sinal conforme o par, o que é incompatível com um efeito puramente genérico. Mas também não é um deslocamento para o perfil do alvo em todos os descritores: a polifonia sobe nos três pares, mesmo quando o alvo tem menos, e a entropia de classes (harmonia) não se move em nenhum que testamos com ela. Leitura prudente: parte do efeito depende da origem/alvo (andamento: duração e notas/s), parte parece comum (polifonia). Com a referência de Joplin acima da de Chopin só em notas/s e abaixo em duração, o contraste de notas/s é o mais limpo.
- **Ressalvas:** n = 7, p mínimo 0,016, vários testes sem correção; amostras não independentes; continuação de 40 notas; "nenhum" já diverge muito da referência de Chopin em notas/s (15,3 contra 9,3), então a origem das sementes (Chopin) gera o seu próprio perfil de partida; três pares só, com um alvo de controle; sem escuta; um só α e camada. Contra "nenhum", nem a duração (p = 0,30) nem notas/s (p = 0,078) chegam a p < 0,05; a evidência de notas/s vem do contraste com o aleatório.

Figura: `figs/descritores_tres_pares.png` (centrado − nenhum, média ± erro padrão entre sementes, para duração média e notas/s nos três pares, com a direção esperada de cada alvo); gerada por `fig_tres_pares.py`.
