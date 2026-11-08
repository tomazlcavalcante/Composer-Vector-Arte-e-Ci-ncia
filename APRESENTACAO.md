# Roteiro da apresentação (13 slides, cerca de 13 minutos, mais slides de reserva)

Artes e Ciência (IMPA Tech). Lucas Barbosa, Thiago Vinicius e Tomaz L. Cavalcante.
Público: colegas e professor de arte e ciência. Pouca matemática; foco na ideia e nas imagens.
Todos os números vêm de `RESULTADOS.md` e `analysis/F6_controles/VALIDADE.md` (linhas 13 a 18 para F9 a F13). Não foi encontrada carta de intenção do grupo no repositório.
Tempo: cerca de 1 minuto por slide (slides 1 e 13 mais curtos; 3, 4, 5 e 8 podem passar de 1 minuto). Faixa de 12 a 14 minutos.

---

## Slide 1. Estilo é o que nos faz reconhecer um compositor, mas o que exatamente reconhecemos?

- **Visual:** texto. Uma frase de abertura sobre Meyer (estilo em níveis: dialeto da época, idioma do compositor, escolhas dentro da obra) e a pergunta "um modelo de IA enxerga isso?". Opcional: o título do ensaio.
- **O número que importa:** nenhum.
- **Fala:** Quando ouvimos uma peça e pensamos "isso parece Chopin", estamos reconhecendo estilo. Usamos de Leonard Meyer a ideia geral de estilo em níveis (o dialeto de uma época, o idioma de um compositor, as escolhas dentro de cada obra), sem citar página. Nossa pergunta é simples: um modelo que só aprendeu a prever música organiza os compositores de modo parecido? Não julgamos se a música gerada é boa; olhamos como o modelo arruma o mundo por dentro.
- **Cuidado:** Meyer aparece como ideia geral. Não atribuir a ele afirmações específicas nem citar páginas (RESULTADOS, "Leitura à luz de Meyer").

## Slide 2. Pedimos a um modelo que prevê música a "impressão digital" de 52 compositores

- **Visual:** `analysis/figs_apresentacao/pipeline.png` (fluxo: acervo, trechos de ~340 notas, modelo, impressão digital da camada 6, média por compositor, saídas mapa/nuvens/forma/andar no espaço).
- **O número que importa:** 2.183 peças, 52 compositores; camada 6 (acurácia 0,35 contra 0,21 na última; acaso 0,019).
- **Fala:** Usamos um modelo que aprendeu a prever o que vem a seguir na música. Mostramos a ele 2.183 peças de piano de 52 compositores e guardamos o que ele "pensa" ao ler cada trecho. A média disso por compositor é a impressão digital dele. Usamos a camada 6, do meio do modelo, porque separa melhor os compositores que a última (acerta 35% em 52 opções, contra 21%). A partir daí tudo é geometria: perto e longe, para o modelo.
- **Cuidado:** o modelo foi treinado no Lakh MIDI, não em música clássica; "perto" e "surpreendente" são relativos a esse treino. As gravações do acervo vêm do YouTube, transcritas automaticamente, então o intérprete e o ruído da transcrição se misturam ao compositor (VALIDADE, "O que nenhum controle cobre").

## Slide 3. O mapa acompanha, em parte, a cronologia, e alguns vizinhos fazem sentido (como ilustração)

- **Visual:** `analysis/F3_geometria/figs/mapa_apresentacao.png`. Mostrar: Bach, Handel e Scarlatti embaixo à esquerda; ragtime em cima à esquerda; românticos e modernos à direita; a estrela do Tico-Tico ao lado do ragtime. Não usar `mapa_pca.png`.
- **O número que importa:** correlação de 0,505 entre distância e diferença de época (nulo: p = 0,0002 em 5.000 permutações).
- **Fala:** Cada ponto é um compositor; o tamanho mostra quantas peças ele tem. Compositores de épocas próximas ficam mais perto: Haydn fica ao lado de Mozart, Debussy ao lado de Cyril Scott. O Tico-Tico no Fubá, de Abreu, que colocamos como teste, caiu ao lado de Nazareth e do ragtime de Johnson e Scott. A relação com o tempo é real, mas moderada, não uma linha do tempo.
- **Cuidado:** o mapa 2D distorce as distâncias (Spearman 0,76; PC1 explica 34% da variância). Vizinhos são ilustração (muitos pares mudam entre 1 e 2 janelas; Bach ↔ Handel não é mútuo, o vizinho de Bach é Scarlatti). Tico-Tico é uma peça só, ilustração; só os 3 primeiros vizinhos se mantêm (C. L. Johnson 0,417, J. Scott 0,444, Nazareth 0,488). Não afirmar que a semelhança é "por razão musical": pode ser harmonia, textura, gênero ou arquivo MIDI. Nacionalidade não mostra efeito detectável ao controlar a época (ρ parcial 0,041, p = 0,111), mas é ausência de evidência.

## Slide 4. O modelo sabe mais que estatística simples: a cronologia sobrevive quando se tiram a superfície e o gênero

- **Visual:** `analysis/F9_superficie/figs/controles_cronologia.png` (barras do Mantel ρ: modelo 0,505; sem gênero 0,379; sem estatísticas de superfície 0,340; só superfície, sem o modelo, 0,204; linha tracejada no nulo ≈ 0,104).
- **O número que importa:** 0,505 → 0,340 sem estatísticas de superfície (e 0,379 sem gênero); só com a superfície, 0,204.
- **Fala:** Uma dúvida natural: será que o modelo só conta notas? Calculamos descritores simples (notas por segundo, altura, duração, polifonia, intervalos), sem o modelo. Um mapa feito só com eles acompanha a época bem menos (0,20 contra 0,50). E, se tiramos esses descritores do modelo, a cronologia continua (0,34); tirando o gênero do título, também (0,38). Então o modelo capta mais do que densidade, registro ou forma. Mas perde de um quarto a um terço da correlação: não é independente da superfície.
- **Cuidado:** controle linear com descritores simples; não remove relações não lineares. Os descritores explicam cerca de 50% da variância do modelo (RSA 0,64), e as classes de altura incluem a tonalidade. Gênero por palavra do título: 52% das peças caem em "outro". As quedas não foram testadas (sem nulo nem IC); p = 0,0002 é o piso. O nulo da figura vale só como referência de ordem de grandeza. O ρ restante não prova que o modelo "conhece a história": pode ser instrumentação, gravação ou transcrição (VALIDADE, linhas 13, 14 e 16).


## Slide 5. Valsas atravessam culturas: para o modelo, a valsa de Nazareth soa perto de Chopin, não do ragtime

- **Visual:** `analysis/F13_brasil/figs/valsas.png` (distância ao ragtime × distância a Chopin; valsas de Nazareth embaixo à direita, tangos e polcas no meio, rags em cima à esquerda, estrela do Tico-Tico no alto). Mostrar logo depois do mapa, que já trouxe o Tico-Tico.
- **O número que importa:** 4 valsas de Nazareth a 0,425 de Chopin, contra 1,087 dos 8 tangos e polcas (p = 0,002, piso do desenho).
- **Fala:** Voltando ao Tico-Tico: Nazareth é o compositor mais próximo do ragtime, mas não todas as peças dele. As quatro valsas verificadas em fontes ficam longe do ragtime e perto de Chopin, e os tangos e polcas fazem o contrário. As valsas do próprio ragtime (Joplin, Johnson) também ficam mais perto de Chopin que os demais rags. Para o modelo, "valsa" atravessa culturas: um gênero de dança agrupa obras de mundos diferentes. Pode ser só o compasso 3/4, e é isso que vamos dizer com cuidado.
- **Cuidado:** exploratório e n muito pequeno (4 valsas, 8 tangos e polcas, 4 valsas de ragtime); p = 0,002 é o mínimo possível e não evidência forte. Valsa é 3/4 e tango e rag são 2/4: o modelo pode captar só o compasso, e andamento lento, textura romântica e transcrição não estão descartados. Rosa Maria vem de fonte comercial (sem ela, p = 0,006); 9 títulos de Nazareth não foram verificados. No gráfico, só 2 das 4 valsas de ragtime ficam bem perto de Chopin (média 0,833 contra 1,215 dos rags, p = 0,0003), e o título da figura cita Joplin, mas uma delas é de C. L. Johnson. Villa-Lobos não mostra fio ragtime. Não afirmar que o modelo "reconhece" a valsa (VALIDADE, linha 18).


## Slide 6. O compositor explica só 28% da variação entre peças no modelo: o estilo é mais nuvem do que ponto

- **Visual:** `analysis/F4_nuvens/figs/nuvens_pecas.png` (as 2.183 peças em cinza e as nuvens de Bach, Mozart, Chopin e Joplin, com elipse de 1 desvio-padrão e centróide, nos mesmos eixos do explorador; Bach e Mozart se sobrepõem muito, Joplin e Chopin ficam isolados; a projeção 2D distorce distâncias). Apoio: `analysis/F4_nuvens/figs/dispersao.png` (rótulos J. Scott e C. Scott já corrigidos). Gerada por `analysis/F4_nuvens/fig_nuvens_pecas.py`.
- **O número que importa:** R² = 0,275 (nulo: 0,0235); 65,3% das peças ficam mais perto do centróide de outro compositor.
- **Fala:** Cada peça é um ponto, e cada compositor é uma nuvem de peças. O compositor explica cerca de 28% da variação entre peças, e dois terços das peças estão mais perto da média de outro compositor do que da própria. Mesmo assim, o modelo acerta o compositor muito acima do acaso. O estilo existe, mas é frouxo: as nuvens se sobrepõem. Uns são compactos (Victoria, ragtime), outros muito espalhados (Heller, Ravina).
- **Cuidado:** o valor depende da representação (de 0,12 a 0,28), mas é sempre uma minoria bem acima do nulo. Os 72% restantes não são "variação de estilo da obra": incluem gênero, forma, tonalidade e ruído de transcrição. A compacidade de Victoria e dos ragtimes pode vir do tipo de arquivo MIDI (não testado). Não dizer que o compositor é "não identificável" (35% de acerto em 52 classes é muito acima do acaso). O compositor pesa mais que o gênero (R² 0,317 contra 0,164, em 1.053 peças), mas isso enfraquece (gênero por palavra do título é impreciso).

## Slide 7. O espaço é um contínuo, com um único corte claro: o bloco pré-romântico

- **Visual:** `analysis/F5_topologia/figs/dendrograma.png`. Apontar o bloco Bach, Handel, Scarlatti, Haydn, Mozart, Beethoven, Hummel se separando cedo, e o resto se juntando de forma gradual.
- **O número que importa:** corte em 2 grupos estável (ARI 0,782 em 100 bootstraps); os cortes em 3, 4 e 5 são instáveis (0,436, 0,567 e 0,565).
- **Fala:** Perguntamos se os compositores formam ilhas ou uma paisagem contínua. A resposta é quase só paisagem: não há lacuna maior do que a de uma nuvem sem grupos. A exceção é um bloco de sete compositores, de Bach a Beethoven, que se separa do resto e continua separado quando refazemos a conta (com pequenas trocas de membros: com 3 janelas por peça o grupo ganha Mendelssohn e Victoria). Os 45 demais, de Chopin ao ragtime, vão se juntando sem fronteira nítida.
- **Cuidado:** com 3 janelas por peça o núcleo se mantém, mas o grupo de k = 2 ganha Mendelssohn e Victoria (ARI 0,753). Chamar o bloco de "pré-romântico", não de "Barroco" (inclui Clássicos), e lembrar que há poucos barrocos (3) e clássicos (4). Com 52 pontos o teste tem pouca potência: não se conclui que "não existem grupos". Só foi medido o grau 0 (nada sobre ciclos ou Mapper). A robustez do bloco é parcial: nas camadas 12 e com o último token, ele vem com intrusos (Victoria, ragtime). Grupos mais finos (k ≥ 3): cai.

## Slide 8. Somar o vetor de Chopin empurra a música, ao longo de um eixo Bach → Chopin, na direção de Chopin, mas sem chegar lá

- **Visual:** `analysis/F7_deslocamento/figs/steering.png` (título já ajustado). Se sobrar tempo, mostrar também `analysis/F7_deslocamento/figs/steering_alfa.png`. Figura alternativa ou de apoio: `analysis/F7_deslocamento/figs/steering_pares.png` (4 pares; "o vetor do compositor desloca a música entre estilos distantes, mas não em todo par"; Haydn → Mozart fica na nota de rodapé).
- **O número que importa:** progresso de 0,684 com o vetor de Chopin, contra 0,433 (vetor aleatório) e 0,392 (sem vetor); 7 de 7 sementes de Bach (p = 0,016).
- **Fala:** Aqui invertemos o caminho: em vez de só olhar, mexemos. Pedimos ao modelo que continue um trecho de Bach somando o vetor médio de Chopin ao seu estado interno. Medimos o resultado numa régua (um eixo) em que 0 é o centro de Bach e 1 é o centro de Chopin: sem vetor, 0,39; com um vetor aleatório, 0,43; com o de Chopin, 0,68. Quanto mais forte o vetor, mais a música avança (de 0,38 a 0,75). Mas a música não vira Chopin: ela avança cerca de dois terços ao longo desse eixo, e continua longe do centro de Chopin.
- **Cuidado:** a distância ao centróide de Chopin continua alta (0,930 em α = 1, contra 1,182 sem vetor; na varredura, de 1,178 para 0,849 em α = 1,5). Testado em 4 pares (3 de 4 direções interpretáveis, todas entre compositores distantes; falha em Joplin → Chopin; Haydn → Mozart não interpretável), 7 sementes, uma peça por semente, sem escuta. O eixo de medida é o mesmo que o vetor empurra. A média sobe com α, mas por semente só 4 de 7 trajetórias são monótonas. A única medida de degeneração (repetição de trigramas) não aumentou até α = 1,5 (médias de 1,5% a 4,1% no experimento principal), mas isso não garante música coerente. No caminho entre Bach e Chopin, o ponto médio (t = 0,5: 0,338) não passa do "sem vetor" (0,392): "Bach domina a mistura" não foi testado (só em Bach ↔ Chopin: enfraquece). Não mostrar a hipótese como "provada".

- **Reforço com medida independente:** com o vetor de Chopin, as notas da música gerada ficam mais longas (0,30 s → 0,65 s; Chopin tem 0,63 s) em 7 de 7 sementes. Ao mesmo tempo ela fica menos densa (9,0 → 4,8 notas por segundo, contra o perfil de Chopin) e mais sobreposta (polifonia 2,4 → 3,0, na direção de Chopin). Frase sugerida: "o vetor muda a textura de um jeito que lembra Chopin em parte, mas não o imita".

- **Generalização:** o efeito se repete em Chopin → Bach e Mozart → Debussy, mas falha em Joplin → Chopin (5/7, p = 0,69). Haydn → Mozart não é interpretável (estão sobrepostos no mapa). Dizer: "funciona entre estilos distantes; não é garantido para qualquer par".

## Slide 9. A surpresa do modelo cresce, em média, com a época, mas é a surpresa deste modelo, não a de um ouvinte

- **Visual:** `analysis/F8_expectativa/figs/surpresa_por_compositor.png`. Apontar Victoria, os barrocos e o ragtime à esquerda da média; Scharwenka, Rzewski, Scriabin e Lack à direita.
- **O número que importa:** correlação de 0,51 entre surpresa do compositor e ano de nascimento (IC95% 0,23 a 0,73; n = 52); com densidade, polifonia e duração controladas, 0,41 (p = 0,002).
- **Fala:** Na ideia geral de Meyer que usamos, expectativa importa para o estilo. Medimos o quanto o modelo se surpreende com cada compositor, a média da perda por token (cada nota tem três tokens). Victoria é o mais previsível para ele e Scharwenka o mais surpreendente. Em média, quanto mais recente o compositor, maior a surpresa: Barroco 2,25, Clássico 2,32, Romântico 2,54, Moderno 2,70. Ragtime e barrocos estão entre os mais previsíveis. E isso não é só densidade de notas: controlando densidade, polifonia e duração, a correlação com a época cai de 0,51 para 0,41, mas não some.
- **Cuidado:** perda baixa não é "música simples" nem "esperada por Meyer": é previsibilidade para um modelo treinado no Lakh. A tendência pode refletir quanto cada repertório aparece no Lakh, ruído de transcrição, gênero e tamanho do acervo (Barroco 3 compositores, Clássico 4). Os descritores simples explicam 72% da surpresa; ritmo e tonalidade de forma mais rica não foram medidos. Os mais surpreendentes não formam um bloco estilístico óbvio. Resultado correlacional, robusto ao nulo por compositor (p = 0,008); com o controle, enfraquece (VALIDADE, linha 15).

## Slide 10. O que o modelo não vê: pedal, andamento, dinâmica e o intérprete

- **Visual:** texto. Lista curta com ícones ou riscos: pedal, andamento, dinâmica, pianista e gravação, "treinado no Lakh, não em música clássica".
- **O número que importa:** janela de no máximo 341 eventos e 100 s por trecho (sem pedal, sem token de andamento, só tempo, duração e nota).
- **Fala:** O modelo só vê três coisas por nota: quando começa, quanto dura e qual é. Pedal e dinâmica não entram, e não há marcação de andamento. Parte do que ouvimos como estilo pode estar justamente aí (não testamos quanto). Além disso, as peças vêm de gravações transcritas automaticamente, então o pianista se mistura ao compositor, e o modelo foi treinado em outro repertório. O mapa é, portanto, o estilo como esse modelo o vê, não como o ouvimos.
- **Cuidado:** a afirmação sobre pedal, dinâmica e andamento vem do código do AMT instalado (`anticipation/convert.py`, mensagens de controle ignoradas) e da extração (`F0_infra/extract_amt.py`), não de um teste. A "linha de base simbólica" (histograma de intervalos, duração, densidade) e o controle de andamento e dinâmica ainda faltam. A transposição pequena mexe pouco (0,02 a 0,03 contra 0,93 entre centróides), mas em 13 de 45 peças (29%) o centróide mais próximo muda: enfraquece; não concluir que o modelo ignora tonalidade. Metadados (nascimento, nacionalidade) curados à mão, não verificados fora.

## Slide 11. À luz de Meyer: o estilo do modelo tem níveis, mas é gradual e frouxo

- **Visual:** `analysis/figs_apresentacao/meyer_niveis.png` (três níveis: época, compositor, obra, cada um com o achado em uma linha; escolhas dentro de restrições e expectativa ficam na fala).
- **O número que importa:** 52 de 52 compositores têm janelas da mesma peça mais próximas entre si do que de outras peças do próprio compositor (diferença 0,33; IC95% 0,29 a 0,36).
- **Fala:** Lendo à luz de Meyer, o modelo parece ter um nível de dialeto de época, que muda de forma gradual, e um idioma de compositor reconhecível mas frouxo. Dentro de cada obra há coerência, em parte: os dois trechos de uma mesma peça se parecem mais entre si do que com outras peças do autor, mas isso se mistura com a gravação e o arquivo MIDI, que são os mesmos nos dois trechos. Um achado exploratório aponta na mesma direção: o gênero valsa agrupa obras de culturas diferentes (slide 5), compatível com convenções compartilhadas acima do compositor. E o vetor médio captura parte das restrições de um estilo, mas a música gerada ainda faz escolhas que ele não fixa. É uma leitura interpretativa, não uma prova de que o modelo "entende" estilo.
- **Cuidado:** a ligação da valsa com convenções compartilhadas é hipótese (n = 4; pode ser só o compasso 3/4). Esta é a seção de interpretação do RESULTADOS; só ligamos aos níveis resultados que sobrevivem. A coesão da obra enfraquece: a medida mistura coerência da peça com a gravação e o arquivo MIDI (os mesmos nas duas janelas) e não mede expectativas dentro da obra. O vetor de Chopin move a música até 0,684 e a distância ao alvo continua 0,930. A expectativa é a do modelo, não a de um ouvinte.

## Slide 12. O que a análise sustenta e o que ela não permite dizer

- **Visual:** texto. Três colunas: "Sobrevive" (época: 0,505, e ainda 0,340 sem superfície e 0,379 sem gênero; compositor explica minoria: 0,275; contínuo com bloco pré-romântico: ARI 0,782; steering parcial: 3 de 4 pares), "Exploratório ou ilustração" (valsas atravessam culturas; Tico-Tico; "à frente ou atrás do tempo") e "Não dizemos" (que o mapa é uma linha do tempo; que a música virou Chopin; que o modelo entende estilo como um ouvinte; que há grupos finos; que os finais de obra são mais convencionais: H13 caiu).
- **O número que importa:** 7 de 7 sementes (p = 0,016, o menor valor possível com 7), e ARI 0,782 só para dois grupos.
- **Fala:** Em resumo, três coisas se sustentam: a distância no modelo acompanha a época, de forma moderada; o compositor explica uma minoria, então estilo é mais nuvem do que ponto; e o espaço é contínuo, com um bloco de Bach a Beethoven. A cronologia sobrevive aos controles de superfície e de gênero, com queda. O deslocamento por vetor funciona de forma parcial, em 3 de 4 direções interpretáveis, todas entre compositores distantes. As valsas são um indício exploratório. Outras coisas enfraquecem ou caem, inclusive a ideia de que os finais de obra são mais convencionais: vizinhos individuais, grupos finos, coesão por obra. Preferimos dizer isso com clareza a vender um resultado mais bonito.
- **Cuidado:** os controles são lineares e simples (VALIDADE, linhas 13 a 16). Usar a coluna "Enfraquece/Cai" da VALIDADE como reserva para perguntas: vizinhos (7, enfraquece), Tico-Tico (8, ilustração), coesão da obra (5, enfraquece), H4 gênero (4, enfraquece), transposição (12, enfraquece), H7 caminho (10, enfraquece), surpresa controlada (15, enfraquece), finais (17, cai). Os p-valores dependem de poucas sementes/permutações: p = 0,016 é o menor possível, não "muito forte".

## Slide 13. Próximos passos: ouvir, controlar o que falta e testar outros pares

- **Visual:** texto. Lista curta, mais o link do explorador interativo, como "material para quem quiser explorar": https://claude.ai/artifact/NeP4zc74AncnZsXsZuLvvo (mapa dos 52 compositores com cor por período, nacionalidade ou surpresa; vizinhos, nuvens de peças, Tico-Tico e setas do steering).
- **O número que importa:** 4 pares interpretáveis (o vetor desloca em 3) e 7 sementes por par: a base do que ainda falta. Também falta testar as valsas com mais peças e controlar o compasso.
- **Fala:** Falta ouvir: não houve escuta das músicas geradas, e esse seria um teste muito mais direto de estilo. Falta testar mais pares de compositores (só 4 foram testados) e outros eixos, controlar andamento, dinâmica e superfície de forma não linear (o controle linear já foi feito), e verificar os metadados em fontes externas. E vale repetir com um modelo treinado em música clássica. Quem quiser explorar o mapa por conta própria pode usar o explorador interativo (link no slide). Para quem faz arte, a pergunta continua aberta: o que, no estilo, é invisível para uma máquina que só vê notas e tempos?
- **Cuidado:** ainda faltam intervalos e nulos para vários números (F2, transposição, vizinhos). Nada disso foi feito; apresentar como proposta, não como resultado.

---

## Slides de reserva (só para perguntas ou se sobrar tempo)

- **R1. As camadas do meio do modelo separam melhor os compositores do que a última.** Figura `analysis/F2_representacao/figs/camadas.png`. Número: 0,35 na camada 6 contra 0,21 na última (acaso 0,019). Cuidado: cada número é uma execução, sem IC; a camada foi escolhida e avaliada nos mesmos dados; não dizer que a 6 é melhor que a 5, 7, 8 ou 9, nem que o modelo "sabe menos" na última camada.
- **R2. À frente ou atrás do tempo (só ilustração).** Figura `analysis/F11_tempo/figs/tempo_vs_mapa.png`. Número: 37 de 52 compositores com IC do resíduo fora de zero. Fala: o ragtime e os clássicos soam "mais antigos" que a data e o romantismo médio e tardio "mais moderno", para o modelo. Cuidado: o IC mede só a amostragem das peças, sem a incerteza da reta (R² 0,35) nem da PCA; desvios de grupo geram resíduos "significativos" em bloco; Victoria tem alavancagem; é posição no mapa, não juízo de inovação. Rótulos de Meyer-Helmund e Scriabin se sobrepõem na figura.
- **R3. Finais de obra: H13 caiu.** Sem figura. Número: Δ −0,0072 (cerca de 1% da distância ao centróide do período; 53,1% das peças); por compositor, 33 de 52 (período) e 26 de 52 (compositor); sinal oposto no Barroco e no Clássico. Fala: procuramos finais mais convencionais e não encontramos evidência.
- **R4. Pares de steering.** `analysis/F7_deslocamento/figs/steering_pares.png`, como no slide 8.

## Figuras a ajustar antes de usar

1. `analysis/F9_superficie/figs/controles_cronologia.png` (slide 4): rótulos e valores em português com vírgula; conferida. O nulo (≈ 0,104) é do espaço do modelo.
2. `analysis/F13_brasil/figs/valsas.png` (slide 5): conferida. O título cita "Joplin", mas entre as valsas de ragtime há uma de C. L. Johnson; fala e legenda devem dizer "ragtime". Considerar fonte maior nos rótulos.
3. `analysis/F4_nuvens/figs/nuvens_pecas.png` (slide 6): conferida (Bach 129, Mozart 72, Chopin 96, Joplin 31 peças); a nota da figura já avisa que a projeção 2D distorce.
4. `analysis/F2_representacao/figs/camadas.png` (reserva R1): rótulos "melhor: camada 6 (0.35)" com ponto decimal; trocar por vírgula.
5. `analysis/F7_deslocamento/figs/steering.png` (slide 8): título cauteloso; considerar remover as três condições de "caminho" (t = 0, 0,5, 1), que levam à leitura "Bach domina", não testada.
6. `analysis/F7_deslocamento/figs/steering_alfa.png`: mostrar só se houver tempo; só 4 de 7 trajetórias são monótonas.
7. `analysis/F7_deslocamento/figs/steering_dois_sentidos.png`: não usada; se for mostrada, não atribuir a assimetria ao vetor.
8. `analysis/F3_geometria/figs/mapa_apresentacao.png` (slide 3): fonte maior nos rótulos; opcional destacar os nomes citados.
9. `analysis/F5_topologia/figs/dendrograma.png` (slide 7): não comentar os cortes finos (k ≥ 3); conferir legibilidade.
10. `analysis/F8_expectativa/figs/surpresa_por_compositor.png` (slide 9): falar sempre "do modelo".
11. `analysis/F11_tempo/figs/tempo_vs_mapa.png` (reserva R2): rótulos sobrepostos no alto; só ilustração.
12. `analysis/F4_nuvens/figs/dispersao.png`: apoio ao slide 6; falta legenda de cores por período.
13. Não usar `analysis/F3_geometria/figs/mapa_pca.png`.

## Sugestão de divisão das falas

- **Lucas Barbosa (slides 1 a 5, cerca de 5 min):** pergunta, Meyer, pipeline e escolha da camada, mapa, o controle de superfície e as valsas. Parte conceitual e de arte.
- **Thiago Vinicius (slides 6, 7 e 8, cerca de 4 min):** nuvem, contínuo e steering. Parte técnica e de modelo.
- **Tomaz L. Cavalcante (slides 9 a 13, cerca de 4 min):** surpresa, o que o modelo não vê, leitura à luz de Meyer, validade e próximos passos (com o explorador interativo). Fecha o ensaio.

Os três podem trocar a divisão; ela é só uma sugestão. Se faltar tempo, cortar o slide 10 (o que o modelo não vê) para uma frase no slide 13 e o slide 7 (contínuo) para uma frase no slide 6. Se sobrar tempo, o slide 8 ganha `steering_alfa.png` e as reservas R2 a R4 ficam à mão.
