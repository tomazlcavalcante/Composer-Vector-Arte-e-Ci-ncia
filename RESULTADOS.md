# Resultados

Ensaio para Artes e Ciência (IMPA Tech). Este texto reúne o que o estudo encontrou, o que se sustenta e o que não se pode concluir. Os números vêm dos `metrics*.json`, dos CSVs e dos REPORTs corrigidos (errata do DIARIO). Quando DIARIO e REPORT divergem, vale o REPORT. O filtro de validade é `analysis/F6_controles/VALIDADE.md`.

## Abertura

Pegamos um modelo que aprendeu a prever música, o Anticipatory Music Transformer small, treinado no Lakh MIDI. Pedimos a ele a "impressão digital" de 2.183 peças de piano do acervo GiantMIDI, de 52 compositores, e fizemos a média por compositor. Em seguida olhamos como o modelo organiza esses compositores no seu espaço interno. A resposta principal: o modelo organiza os compositores de forma parcialmente cronológica, com um bloco pré-romântico (Bach a Beethoven) à parte, mas sem grupos nítidos. O compositor explica só uma minoria (28%) da variação entre peças, então o estilo, nesse espaço, é mais nuvem do que ponto. Somar o vetor de Chopin aumenta, de forma parcial, a projeção da música gerada no eixo Bach → Chopin (mais do que um vetor aleatório), e isso foi medido com um único par de compositores.

## Como ler os vereditos

- **Sobrevive:** nenhum controle ameaça a afirmação.
- **Enfraquece:** vale, com ressalva.
- "Camada 6, média" é a representação escolhida na F2 (a menos que se diga outra).

## Q0. Qual representação do modelo usar? (F2)

**Resposta.** As camadas do meio separam melhor os compositores do que a última, e a média da janela é melhor do que o último token.

**Números.**
- Acurácia balanceada (regressão logística, 5 dobras, divisão por peça; 52 classes): camada 6 com média = 0,349; camada 12 (última) com média = 0,211. Último token: 0,203 na camada 5 e 0,084 na 12.
- Acaso = 1/52 = 0,019. Todas as camadas com média ficam acima (mínimo 0,172, camada 0).
- Estabilidade dos centróides (duas metades das peças): 0,834 na camada 6.
- Sem intervalo de confiança nem nulo por permutação: cada número é uma execução.

**Veredito.** A hipótese da F2 (camadas intermediárias ≥ última) se confirma na direção. Não é uma linha da VALIDADE; a ressalva está no REPORT da F2.

**O que NÃO se pode concluir.**
- Que a camada 6 é melhor que a 5, 7, 8 ou 9: a diferença é de 0,007 a 0,017, sem intervalo. A 5 é a secundária.
- Que o modelo "sabe" menos na última camada: a camada 12 pode estar especializada em prever o próximo token (interpretação, não testada).
- Acurácia de 0,35 em 52 classes está bem acima do acaso, mas é baixa em termos absolutos.
- A camada foi escolhida e avaliada nos mesmos dados.

## Q1. Quem fica perto de quem? (F3)

**Resposta.** Compositores de épocas próximas ficam mais perto no espaço do modelo, mas a relação é moderada; a nacionalidade não mostra efeito detectável quando se controla a época.

**Números.**
- Distância entre centróides × diferença de ano de nascimento (H1): Mantel ρ = 0,505, p = 0,0002 (5.000 permutações; é o menor p possível). Em outras representações, ρ = 0,49 (camada 5), 0,42 (camada 12) e 0,41 (último token); todas com p ≤ 0,001 (1.000 permutações).
- Nacionalidade (H2): ρ = 0,083 (p = 0,019); controlando a época, ρ = 0,041 (p = 0,111). Nas outras configurações o ρ parcial fica entre 0,01 e 0,04, sem intervalo.
- Controle de transposição: mover a peça ±2 ou ±5 semitons desloca o vetor em 0,022–0,027, contra 0,93 entre centróides (45 peças, 1 janela, sem nulo nem intervalo).
- Mapa 2D (PCA): PC1 explica 33,5% e PC2 19,6% da variância dos centróides. PC1 × ano de nascimento: ρ = 0,525 (PC2: 0,26). O mapa distorce as distâncias reais (Spearman 0,76).
- Vizinhos mais próximos (ilustração; os IC são largos): Haydn ↔ Mozart 0,101 [0,082; 0,186]; J. Scott ↔ C. L. Johnson 0,075 [0,066; 0,117]; Debussy ↔ C. Scott 0,157 [0,123; 0,385]; Medtner ↔ Schumann 0,236 [0,210; 0,508]. Bach ↔ Handel não é mútuo (o vizinho de Bach é Scarlatti, 0,200 [0,160; 0,260]). Satie → Rebikov (0,284 [0,221; 0,456]) também não é mútuo (o vizinho de Rebikov é Scharwenka). Chopin → Grieg tem IC de 0,249 a 0,614.
- Tico-Tico (uma peça): vizinhos C. L. Johnson (0,417), J. Scott (0,444), Nazareth (0,488).

**Veredito.**
- Época (H1): **sobrevive**.
- Nacionalidade (H2): **sobrevive, com cautela** (ausência de evidência, não evidência de ausência; teste de pouca potência; metadados não verificados fora).
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
- R² do compositor (H3) = 0,275. Nulo (200 permutações de rótulos): média 0,0235, p95 0,0254. Nas outras representações, R² de 0,26 (camada 5), 0,22 (camada 12) e 0,12 (último token).
- 65,3% das peças ficam mais perto do centróide de outro compositor. Mesmo assim, o acerto médio por compositor é 0,346, contra cerca de 0,019 ao acaso.
- Gênero (H4; 1.053 peças com gênero por palavra-chave do título): R² do gênero = 0,164, do compositor nas mesmas peças = 0,317. Distância média: mesmo compositor e gênero diferente 0,779; mesmo gênero e compositor diferente 0,940.
- Mais compactos (n igualado em 20): Victoria 0,085, C. L. Johnson 0,258, Meyer-Helmund 0,277, J. Scott 0,297, Joplin 0,424. Mais espalhados: Heller 0,900, Ravina 0,897, Gurlitt 0,886, Moszkowski 0,872, Mendelssohn 0,871 (empate prático com Schubert, 0,8706).
- Dentro da obra: janelas da mesma peça ficam a 0,434 uma da outra; peças diferentes do mesmo compositor, a 0,789; compositores diferentes, a 1,005. Em 52 de 52 compositores, as janelas da mesma peça ficam mais próximas entre si do que de outras peças do mesmo compositor (diferença 0,33, IC95% 0,29–0,36).
- R² bruto "da peça" = 0,78, mas o nulo por construção (2 janelas por peça) é 0,50; corrigido, 0,57. Não comparar com o R² do compositor.

**Veredito.**
- Compositor explica minoria (H3): **sobrevive** (o número exato depende da representação, de 0,12 a 0,28; é sempre uma minoria bem acima do nulo).
- Compositor pesa mais que gênero (H4 não se confirma): **enfraquece** (R² não ajustado pelo número de grupos, gênero por título é impreciso, sem intervalo).
- Obra mais coesa que o compositor: **enfraquece** (confundido com gravação e arquivo MIDI, que são os mesmos nas duas janelas).
- "Originalidade" = distância bruta à média geral; o número de peças não correlaciona com ela (ρ = −0,116). O z de originalidade cresce com n por construção (ρ = 0,461) e não deve ser usado.

**O que NÃO se pode concluir.**
- Que o compositor não é identificável: 35% de acerto em 52 classes é muito acima do acaso.
- Que os 72% restantes são "variação de estilo da obra": incluem gênero, forma, tonalidade e ruído de transcrição, sem decomposição.
- Que Victoria e os ragtimes têm estilo mais coeso: a compacidade pode vir do tipo de arquivo MIDI (não testado). Victoria tem exatamente 20 peças.
- A ordem dos mais espalhados é instável (mudou entre 1 e 2 janelas por peça); a dos mais compactos, não.
- As obras atípicas (a mais atípica: "Wedding of the Fairies Waltz" de Johnson, z = 4,47) são só para leitura qualitativa.

## Q3. Grupos ou contínuo? (F5)

**Resposta.** O espaço é um contínuo, com um único corte estável: os sete compositores pré-românticos de um lado e os outros 45 do outro.

**Números.**
- Maior barra de H0 = 0,515; mediana = 0,291; razão = 1,769, contra p95 do nulo gaussiano de 2,31. Não há lacuna maior do que a de uma nuvem sem grupos (200 gaussianas).
- Corte em 2 grupos (ligação média): ARI em 100 bootstraps de peças = 0,782. Grupo de 7: Bach, Beethoven, Handel, Haydn, Hummel, Mozart, Scarlatti. Grupo de 45: todo o resto, inclusive Victoria.
- Cortes em 3, 4 e 5: ARI = 0,436, 0,567 e 0,565 (instáveis; a composição mudou entre 1 e 2 janelas por peça).
- Nas camadas 5 e 6 o bloco é o mesmo; nas camadas 12 e com último token ele vem com intrusos (Victoria, ragtime).

**Veredito.** Contínuo e bloco pré-romântico: **sobrevive**. Grupos mais finos (k ≥ 3): **cai**. A robustez do bloco entre representações é parcial.

**O que NÃO se pode concluir.**
- Que não existem grupos: com 52 pontos o teste tem pouca potência.
- Que o ramo destacado é "o Barroco" (H5): o grupo inclui Clássicos. Chamar de pré-romântico.
- Nada sobre ciclos (grau 1) ou Mapper: só foi medido o grau 0.
- Os grupos vêm da ligação média e o teste de lacuna, da ligação simples; o ARI mede só o primeiro. O nulo gaussiano não preserva a forma real da distribuição.

## Q4. Somar o vetor de um compositor desloca a música? (F7)

**Resposta.** Somar o vetor centrado de Chopin na camada 6 aumenta a projeção da continuação, relida sem steering, no eixo Bach → Chopin, mais do que um vetor aleatório ou nenhum vetor. O deslocamento é parcial e foi medido com um único par.

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
- Progresso monótono no caminho Bach → Chopin (H7): **enfraquece** (um par só; 7 sementes).

**O que NÃO se pode concluir.**
- Que a música "virou Chopin": o progresso de 0,68 é a projeção num eixo, e a distância ao centróide de Chopin continua em 0,930 (α = 1, experimento principal; 1,182 sem steering).
- Que "Bach domina a mistura": a observação é descritiva, sem teste. A diferença entre t = 0,5 (0,338) e "nenhum" (0,392) é menor que 2 erros padrão.
- Que o efeito é menor no sentido inverso por causa do vetor: a comparação mistura eixos, sementes, bases de centróides (1 contra 2 janelas) e n (14 contra 7). As continuações de Chopin sem steering repetem mais trigramas (0,124 contra 0,041).
- Que não há quebra: não vimos aumento da repetição até α = 1,5, mas isso não garante música coerente. Não houve escuta nem outro par, outro eixo ou outra métrica. O eixo de medida é o mesmo que o vetor centrado empurra.
- Que os pontos intermediários caem perto dos clássicos: isso só foi visto na geometria, não no steering.

**Outros pares** (`analysis/F7_deslocamento/pares_resumo.csv`; 7 sementes, 1 amostra por condição, α = 1, centróides de 2 janelas, exceto Bach → Chopin, que usa a base "forte" de 1 janela):

| Par | Distância entre centróides | Nenhum | Aleatório | Centrado | Centrado > aleatório |
|---|---|---|---|---|---|
| Bach → Chopin | 1,60 | 0,39 | 0,43 | 0,68 | 7/7 (p = 0,016) |
| Chopin → Bach | 1,60 | 0,33 | 0,29 | 0,46 | 7/7 (p = 0,016) |
| Mozart → Debussy | 1,71 | 0,23 | 0,28 | 0,50 | 6/7 (p = 0,031) |
| Joplin → Chopin | 1,11 | 0,44 | 0,49 | 0,55 | 5/7 (p = 0,69) |
| Haydn → Mozart | 0,10 | — | — | — | não interpretável |

O efeito se repete em 3 das 4 direções interpretáveis e falha em Joplin → Chopin. Haydn e Mozart estão quase sobrepostos no mapa (distância de 0,10), então o eixo "origem → alvo" não está bem definido e o progresso sai do intervalo 0–1. **Leitura:** H6 deixa de depender de um par só, mas não vale para qualquer par. Nos três pares em que funcionou, os compositores estão distantes no mapa (distância ≥ 1,6). Com 4 pares, a relação entre distância e efeito é só sugestiva.

**Checagem com descritores independentes do modelo** (`analysis/F7_deslocamento/metrics_descritores.json`; 7 sementes de Bach × 2 amostras, continuações de 40 notas, vetor centrado de Chopin com α = 1). Medimos a música gerada sem usar o modelo, com estatísticas simples das notas. O resultado é misto:
- **Vão na direção de Chopin:** a duração média das notas sobe de 0,30 s para 0,65 s em 7 de 7 sementes (referência: Bach 0,37 s, Chopin 0,63 s). A polifonia sobe de 2,4 para 3,0 (6 de 7 contra a condição sem steering; 7 de 7 contra o aleatório). A dispersão das alturas aumenta em relação ao vetor aleatório (7 de 7).
- **Vão contra:** as notas por segundo caem de 9,0 para 4,8 (7 de 7), embora Chopin seja mais denso que Bach na referência (9,3 contra 8,0). A altura média cai cerca de 3 semitons.
- **Leitura cautelosa:** o vetor muda de fato a textura (notas mais longas, mais sobrepostas, música mais "lenta"), e parte dessa mudança coincide com o perfil de Chopin. Mas não é uma imitação de Chopin em todos os aspectos. Com 7 sementes, um par só e descritores simples, isso é indício, não prova.

## Q5. Expectativa: o quanto o modelo se surpreende? (F8)

**Resposta.** A surpresa do modelo varia entre compositores e cresce, em média, com a época; isso é surpresa **para este modelo**, não expectativa de um ouvinte.

**Números** (perda média por token, em nats).
- Média das peças: 2,49 (dp 0,48 entre peças; 0,31 entre compositores). Menor: Victoria 1,74. Maior: Scharwenka 3,32, depois Rzewski 3,22, Scriabin 3,17, Lack 3,16, Fauré 2,91.
- Mais previsíveis depois de Victoria: C. L. Johnson 1,94, Raff 1,94, J. Scott 2,08, Nazareth 2,20, Joplin 2,20, Handel 2,21. Bach 2,28, Scarlatti 2,25 e Beethoven 2,25.
- Compositor × nascimento: ρ = 0,51 (IC95% 0,23–0,73; p = 1,2e-4; n = 52).
- Por período (peças): Barroco 2,25 (3 compositores), Clássico 2,32 (4), Romântico 2,54 (33), Moderno 2,70 (11). Kruskal-Wallis H = 243, ε² = 0,11; permutando o período entre compositores, p = 0,008.
- O compositor explica η² = 0,37 da surpresa entre peças (nulo: média 0,024, p95 0,032).
- Confiabilidade: Spearman entre janela 1 e janela 2 = 0,72 dentro da peça; 0,98 entre médias por compositor.

**Veredito.** Não está na VALIDADE.md (a F8 veio depois). O REPORT da F8 trata o efeito de época como robusto ao nulo por compositor (p = 0,008), mas correlacional.

**O que NÃO se pode concluir.**
- Que perda baixa é "música simples" ou "esperada por Meyer": é previsibilidade para um modelo treinado no Lakh.
- Que a regularidade de tonalidade e ritmo explica a ordem: não foi medida (nenhum controle de densidade de notas). Compatível com ragtime e maxixe no extremo previsível, mas Raff e Victoria também estão lá, e os mais surpreendentes (Scharwenka, Lack, Rzewski) não formam um bloco estilístico óbvio.
- A tendência com a época pode refletir quanto cada repertório aparece no Lakh, o ruído da transcrição automática, o gênero e o tamanho do acervo (Renascimento tem 1 compositor, Barroco 3, Clássico 4).

## Hipóteses

| Hipótese | Previsão | Resultado | Veredito |
|---|---|---|---|
| F2 | Camadas intermediárias ≥ última | Média: camada 6 = 0,349 contra camada 12 = 0,211; último token: 0,203 (camada 5) contra 0,084 (12). A 6 não se distingue da 5, 7, 8 e 9. | Confirma na direção; sem intervalo |
| H1 | Distância entre centróides cresce com a diferença de época | Mantel ρ = 0,505, p = 0,0002; 0,41–0,49 nas outras representações | Sobrevive; efeito moderado |
| H2 | Nacionalidade pesa menos e pode sumir ao controlar a época | ρ = 0,083 (p = 0,019); parcial 0,041 (p = 0,111) | Sobrevive, com cautela (sem evidência de efeito) |
| H3 | O compositor explica uma minoria da variância entre peças | R² = 0,275 (nulo 0,0235); 65,3% das peças mais perto de outro centróide | Sobrevive; o valor depende da representação (0,12–0,28) |
| H4 | O gênero rivaliza com o compositor | R² do gênero 0,164 contra 0,317 do compositor (1.053 peças) | Não se confirma; enfraquece |
| H5 | O espaço é um contínuo; o ramo destacado, se houver, é o Barroco | Razão 1,769 contra p95 do nulo 2,31; corte em 2 estável (ARI 0,782), bloco de 7 pré-românticos | Contínuo sobrevive; ramo é pré-romântico, não só Barroco; k ≥ 3 cai |
| H6 | O vetor centrado desloca mais que o aleatório e que nenhum, de forma monótona em α | 0,684 contra 0,433 e 0,392 (α = 1); 7 de 7 sementes, p = 0,016; média sobe até α = 1,5 (0,755), mas só 4 de 7 trajetórias são monótonas | Sobrevive, como deslocamento parcial |
| H7 | O progresso Bach → Chopin é monótono; intermediários perto dos clássicos é pergunta aberta | t = 0 → 0,277; 0,5 → 0,338; 1 → 0,688 (monótono, não linear); Mozart e Beethoven são os clássicos mais próximos do segmento (geometria) | Enfraquece (um par; sem teste para "Bach domina") |

## Leitura à luz de Meyer

Esta seção é interpretação. Usa a ideia geral de que o estilo se organiza em níveis (do dialeto de uma época até as escolhas dentro de uma obra) e de que expectativa e surpresa importam. Não atribuímos a Meyer afirmações específicas que não conferimos, e não há citações nem páginas. Só ligamos aos níveis os resultados que sobrevivem.

- **Dialeto, época (H1, H5):** a distância crescer com a diferença de nascimento (ρ = 0,505) e o bloco pré-romântico se separar de modo estável (ARI 0,782) são compatíveis com a ideia de que as épocas compartilham um dialeto. O fato de o espaço ser contínuo e o PC1 acompanhar a cronologia só em parte (ρ = 0,525) sugere que o dialeto muda gradualmente, sem fronteiras nítidas. Lembrar que há poucos barrocos e clássicos.
- **Idioma do compositor (H3):** o compositor explica uma minoria da variação (R² = 0,275, nulo 0,0235), e o acerto médio de 0,346 é muito acima do acaso. Isso sugere que há um idioma reconhecível por compositor, mas frouxo: a nuvem de cada um se sobrepõe à dos vizinhos. É uma leitura do modelo, que vê só notas e tempos.
- **Estilo interno da obra:** janelas da mesma peça são mais próximas entre si do que de outras peças do mesmo compositor (52 de 52). É compatível com a ideia de que cada obra tem uma coerência própria. Mas nossa medida mistura essa coerência com a gravação e o arquivo MIDI, e não mede as expectativas dentro da obra. Por isso fica como indício fraco.
- **Escolhas dentro de restrições (H6, H7):** somar o vetor de Chopin move a continuação no eixo (0,684 contra 0,392 sem steering; 7 de 7 sementes), mas a música não chega ao centróide dele (distância 0,930). Uma leitura possível, sem teste direto, é que o vetor médio captura uma parte da restrição de um estilo, e a música gerada ainda faz escolhas que o vetor não fixa. O caminho Bach → Chopin só foi testado em um par.
- **Expectativa (F8):** a surpresa do modelo cresce, em média, com a época (ρ = 0,51, IC95% 0,23–0,73), e os ragtimes e os barrocos estão entre os mais previsíveis. Não distinguimos entre repertório mais ou menos presente no Lakh e regularidade da própria música. Mas a expectativa aqui é a de um modelo treinado no Lakh, não a de um ouvinte, e a regularidade de tonalidade e ritmo não foi medida.

## O que o modelo não vê / limitações

- **Pedal, andamento e dinâmica.** No código do AMT instalado (`anticipation/convert.py`), as mensagens de controle, que incluem o pedal, são ignoradas ("ignore for now"). Os eventos usados na extração têm só três campos: tempo, duração e nota (`F0_infra/extract_amt.py`). Não há token de andamento: o tempo é medido em segundos reais, que vêm da execução transcrita. Marcações de dinâmica (velocity) não entram nesses eventos. O `use_tempos = false` e o `use_sustain_pedals = false` do PLANO.md e do `tokenizer_config.json` descrevem o tokenizador (miditok) do modelo original do repositório; o AMT usado nos resultados tem tokenização própria, e a leitura acima vem do código dele. A janela é limitada a 341 eventos e a 100 s.
- **Pianista e gravação.** O GiantMIDI transcreve gravações do YouTube. O intérprete se mistura com o compositor, e a transcrição automática adiciona ruído. Isso afeta sobretudo a coesão por obra e a surpresa.
- **Modelo.** O AMT foi treinado no Lakh MIDI, não em música clássica. "Perto" e "surpreendente" são relativos a esse treino.
- **Amostra.** Poucos compositores barrocos (3), clássicos (4) e do Renascimento (1). Só 52 compositores.
- **Metadados.** Nascimento e nacionalidade foram curados à mão e não verificados em fonte externa. A verificação por web foi bloqueada no ambiente.
- **Mapa 2D.** Distorce as distâncias (Spearman 0,76). Serve para ilustrar; as medidas são feitas no espaço original.
- **Escolha de representação.** Camada, pooling e número de janelas mudam parte dos números (o R² do compositor vai de 0,12 a 0,28). A camada foi escolhida e avaliada nos mesmos dados.
- **Steering.** Um par, sete sementes de Bach, uma peça por semente, sem escuta. O progresso é uma projeção num eixo.
- **Controles que faltam.** Andamento, dinâmica e linha de base simbólica (histograma de intervalos, duração, densidade). Também faltam IC e nulo para vários números (F2, transposição, vizinhos).
- **Nomes.** Várias listas usam só o sobrenome; "Scott" pode ser J. Scott ou C. Scott.
- **Estabilidade (teste com 3 janelas por peça; fonte: `analysis/F6_controles/metrics_3janelas.json`).** O núcleo pré-romântico se mantém, mas o bloco do corte em k = 2 ganha Mendelssohn e Victoria (9 compositores, ARI 0,753, razão de lacuna 1,732 contra p95 2,372). Fora isso, os resultados mudam pouco: camada 6 média com acurácia balanceada 0,368; Mantel ρ = 0,506 (p = 0,0002); nacionalidade parcial ρ = 0,041 (p = 0,114); R² do compositor 0,299 (63,9% das peças mais perto de outro centróide); H4: R² do gênero 0,179 contra 0,337. A base principal continua sendo 2 janelas.

## Figuras candidatas para a apresentação

Todas foram abertas e conferidas.

1. `analysis/F3_geometria/figs/mapa_apresentacao.png`. O mapa dos 52 compositores: Bach, Handel e Scarlatti ficam embaixo à esquerda, ragtime em cima à esquerda e os românticos e modernos para a direita. Mensagem: o eixo principal acompanha, em parte, a cronologia (distorção 0,76). O PC1 está invertido para o tempo crescer para a direita. Distingue J. Scott de C. Scott. É a figura mais forte para abrir.
2. `analysis/F3_geometria/figs/dist_vs_epoca.png`. Dispersão de cada par de compositores. Mensagem: a distância cresce com a diferença de época (Mantel ρ = 0,50, p = 0,0002), mas a nuvem é larga. Para além de cerca de 200 anos a distância deixa de crescer (e parece cair), e os poucos pares envolvem Victoria. Usar como figura de apoio.
3. `analysis/F5_topologia/figs/dendrograma.png`. Dendrograma dos centróides. Mensagem: o bloco Bach–Handel–Mozart–Haydn–Scarlatti–Beethoven–Hummel se separa cedo, e o resto vai se juntando de forma gradual (ARI do corte em 2: 0,782). Distingue J. Scott de C. Scott. Os cortes finos são instáveis (cuidado ao comentar).
4. `analysis/F5_topologia/figs/h0_barras.png`. Barras de fusão contra o nulo gaussiano de 90%. Mensagem: a maior fusão (0,515) fica dentro da faixa do nulo, ou seja, não há lacuna fora do que uma nuvem sem grupos produz (razão 1,769, p95 do nulo 2,31). Na figura, a maior parte da curva fica abaixo da faixa (fusões mais curtas que as de gaussianas): não ler como "curva dentro da faixa".
5. `analysis/F4_nuvens/figs/dispersao.png`. Dispersão intra-compositor com n = 20. Mensagem: ragtime, Meyer-Helmund e Victoria são compactos; Heller, Ravina e Gurlitt são espalhados. J. Scott (0,297) e C. Scott (0,697) aparecem como barras separadas. A compacidade pode vir do arquivo MIDI.
6. `analysis/F2_representacao/figs/camadas.png`. Acurácia por camada. Mensagem: as camadas do meio separam melhor os compositores do que a última (0,35 na camada 6; 0,21 na 12; acaso 0,019); o último token é pior que a média. Os rótulos usam ponto decimal (0.35). Sem intervalo de confiança.
7. `analysis/F7_deslocamento/figs/steering_alfa.png`. Varredura de α. Mensagem: quanto mais forte o vetor de Chopin, mais a continuação avança no eixo Bach → Chopin (0,38 a 0,75), e o vetor aleatório fica plano (0,38 a 0,47). O subtítulo diz "Repetição de trigramas não aumenta até α = 1,5", o que não garante música coerente. Por semente, só 4 de 7 são monótonas.
8. `analysis/F7_deslocamento/figs/steering.png`. Progresso por condição, α = 1, n = 14. Mensagem: o vetor centrado (0,68) fica bem acima do aleatório (0,43) e de nenhum (0,39), e o vetor de Bach sozinho piora (0,28). O título ("empurra a música gerada na direção de Chopin, sem chegar lá") já traz a ressalva: a música não chega ao alvo (a linha tracejada em 1,0). As colunas "caminho" repetem o centrado (t = 1) e levam à leitura "Bach domina", não testada.
9. `analysis/F7_deslocamento/figs/steering_dois_sentidos.png`. Bach → Chopin e Chopin → Bach. Mensagem: o efeito aparece nos dois sentidos (o título da figura diz "mais de Bach para Chopin", que é descritivo) (0,68 contra 0,39 e 0,43; 0,46 contra 0,33 e 0,29), menor no inverso. A comparação mistura eixos, sementes e n (14 contra 7); mostrar sem atribuir a assimetria ao vetor.
10. `analysis/F8_expectativa/figs/surpresa_por_compositor.png`. Surpresa do modelo por compositor, em ordem de nascimento. Mensagem: Victoria, barrocos e ragtime ficam à esquerda da média (2,49), e Scharwenka, Rzewski, Scriabin e Lack ficam bem à direita; a tendência com a época é moderada (ρ = 0,51, IC95% 0,23–0,73). É surpresa para este modelo. Os IC variam bastante entre compositores.

Não recomendada: `analysis/F3_geometria/figs/mapa_pca.png` é a versão de trabalho do mapa. Tem rótulos sobrepostos e dois "Scott" sem distinção; usar a de apresentação.
