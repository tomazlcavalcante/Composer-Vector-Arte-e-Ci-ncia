# F4 — Ponto contra nuvem (Q2)

## Pergunta
Quanto da variação entre peças é explicado pelo compositor? O estilo é um ponto ou uma nuvem?

## Hipótese registrada
- **H3:** o compositor explica uma minoria da variância entre peças (o estilo é mais nuvem que ponto).
- **H4:** o gênero da peça rivaliza com o compositor na organização local.

## Configuração
- Camada 6, pooling média, nível de peça (2.183 peças, 52 compositores; cada peça é a média de 2 janelas, passada 2, números finais do ensaio), espaço centrado, norma 1.
- Variância explicada: R² multivariado (traço entre / traço total). Nulo: 200 permutações de rótulos.
- Dispersão por compositor com n igualado: 200 sorteios de 20 peças.
- Sobreposição: fração das peças mais perto do centróide de outro compositor (o centróide próprio é recalculado sem a peça).
- Gênero (H4): palavra-chave no título, 16 gêneros. Só 1.053 peças têm gênero; as demais ficam como "outro" e saem.
- Obras atípicas: z da distância da peça ao próprio centróide, dentro do compositor.

## Resultado
- **H3:** R² do compositor = 0,275. Nulo: média 0,0235, p95 0,0254.
- **Sobreposição:** 65,3% das peças ficam mais perto do centróide de outro compositor. Em `acerto_centroide.csv`, o acerto médio por compositor é 0,346.
  - Acerto de 1,00 em Victoria, 0,97 em Meyer-Helmund, 0,81 em C. L. Johnson, 0,76 em Hitz, 0,75 em J. Scott, 0,74 em Joplin.
  - Acerto de 0 em Lack e Ravina; Schumann (0,03), Villa-Lobos, Rachmaninoff e Busoni (0,05) quase nunca acertam.
- **H4** (1.053 peças com gênero):
  - R² do gênero = 0,164; R² do compositor nas mesmas peças = 0,317.
  - Distância média entre peças: mesmo compositor e mesmo gênero 0,635; mesmo compositor e gênero diferente 0,779; mesmo gênero e compositor diferente 0,940; tudo diferente 1,018.
- **Dispersão (n = 20):** mais compactos Victoria (0,085), C. L. Johnson (0,258), Meyer-Helmund (0,277), J. Scott (0,297), Joplin (0,424). Mais espalhados Heller (0,900), Ravina (0,897), Gurlitt (0,886), Moszkowski (0,872), Mendelssohn (0,871). A quinta posição é um empate prático: Schubert (0,8706, n = 96) fica a 0,0003 de Mendelssohn (0,8709, n = 24).
- **Atípicas** (`obras_atipicas.csv`): a mais atípica continua sendo "Wedding of the Fairies Waltz" de Johnson (z = 4,47, mais perto de Nazareth). Seguem "Solace" de Joplin (z = 4,25, mais perto de Rebikov) e a Fuga em lá menor B.144 de Chopin (z = 3,66, mais perto de Raff).
- **Passada 1 (1 janela), para comparar:** R² do compositor 0,230; sobreposição 68,8%; H4 com R² do gênero 0,133 e do compositor nas mesmas peças 0,269. Os mais compactos são os mesmos cinco (Victoria, Johnson, Meyer-Helmund, J. Scott, Joplin). Os mais espalhados mudaram em parte (antes Schubert, Schumann, Tchaikovsky, Busoni, Heller; agora só Heller se mantém), então a ordem dos espalhados é menos estável que a dos compactos. As conclusões de H3 e H4 não mudaram.

## Comparação com o nulo
- R² do compositor (0,275) é mais de 11 vezes o nulo (0,0235) e fica muito acima do p95 do nulo (0,0254).
- H4 não tem nulo próprio.

## O que não se pode concluir
- H3: o compositor explica 28% da variância. "Minoria" vale, e o efeito é real contra o nulo. Mas os 72% restantes inclui gênero, forma, tonalidade e ruído de transcrição, sem decomposição aqui.
- Os 65,3% não significam que o compositor não é identificável. O acerto de 35% é muito maior que o acaso de cerca de 1,9% (1/52). Mostram que a nuvem de um compositor se sobrepõe às de outros.
- H4 "não se confirma": o compositor pesa mais que o gênero (0,317 contra 0,164; 0,779 contra 0,940 nas distâncias). Cuidados:
  - o R² cresce com o número de grupos (52 compositores contra 16 gêneros) e não foi ajustado; as distâncias não têm esse problema;
  - o gênero vem de palavra-chave no título e só cobre 1.053 das 2.183 peças;
  - não há intervalo de confiança.
- Compacto não quer dizer estilo coeso. Victoria tem exatamente 20 peças, e não se sabe se a compacidade vem da música ou do tipo de arquivo MIDI. Isso não foi testado.
- A dispersão depende do n igualado em 20. Outro n pode mudar a ordem; entre as passadas 1 e 2, a lista dos espalhados já mudou.
- As obras atípicas são para leitura qualitativa. Não foram verificadas à mão.

## Estilo interno da obra (Meyer)
Pergunta: quanto do "estilo" já está dentro de uma única obra? Análise `intra_obra.py` → `metrics_intra_obra.json`, com as peças que têm 2 janelas (a do meio e a de 1/6; todas as 2.183), camada 6, média, espaço centrado, cosseno.

| distância cosseno média | valor |
|---|---|
| entre janelas da mesma peça | 0,434 |
| entre peças diferentes do mesmo compositor | 0,789 |
| entre compositores diferentes | 1,005 |

- Variância entre janelas explicada pela peça: R² bruto = 0,783. Explicada pelo compositor: R² bruto = 0,224.
- **Nulo por construção:** com apenas 2 janelas por peça, rótulos de pares aleatórios já dão R² ≈ (G−1)/(N−1) = 0,4999 (simulado: 0,4997). Corrigido pelo acaso, (0,7828 − 0,4999)/(1 − 0,4999), o R² por peça é 0,57. Para o compositor por janela o nulo é ≈ 0,013 (permutado: 0,0127), e o corrigido é (0,2242 − 0,013)/(1 − 0,013) = 0,214. Os dois R² brutos têm números de grupos muito diferentes (cerca de 2.183 peças contra 52 compositores) e não são comparáveis; não se deve ler "78% contra 22%" como a peça pesar 3,5 vezes mais.
- Conferência no nível de peça com 2 janelas: R² do compositor = 0,275 (é o número de H3 acima).

**Leitura (cautelosa):**
- Duas janelas da mesma obra ficam bem mais perto uma da outra (0,43) do que duas obras do mesmo compositor (0,79), e estas só um pouco mais perto do que obras de compositores diferentes (1,01). O resultado mais robusto é a comparação direta: em 52 de 52 compositores, as janelas da mesma peça ficam mais próximas entre si do que de outras peças do mesmo compositor (diferença 0,33, IC95% 0,29–0,36). O R² bruto de 0,78 deve ser lido contra o nulo de ~0,50 do desenho de 2 janelas (corrigido: 0,57). O compositor aparece como um agrupamento mais frouxo das peças. Esse padrão é confundido com a gravação e o arquivo MIDI, que são os mesmos nas duas janelas.
- Isso é coerente com a imagem de "nuvem" de H3: parte da dispersão do compositor é variação entre obras, não ruído dentro delas.
- Limites: o R² por peça se apoia em só 2 janelas por peça (nulo de ~0,50 por construção, acima) e não tem IC. As duas janelas de uma peça compartilham tonalidade, textura, andamento e o arquivo MIDI, então "identidade da obra" mistura estilo da obra com características do arquivo; isso não foi separado. O R² do compositor entre janelas (0,224) e entre peças (0,275) têm unidades diferentes (janela contra média de 2 janelas) e não devem ser lidos como a mesma quantidade.
- Não é uma medida direta do "estilo interno" no sentido musical de Meyer (expectativas dentro da obra), e sim da variação do vetor do modelo entre trechos de uma mesma peça.

## Figuras
- [Dispersão por compositor](figs/dispersao.png)

## Ideias fora do escopo
- Direções de desvio por compositor; gênero contra compositor com modelo misto (previstos como "depois").
- IC bootstrap para o R² e para o R² do gênero, com nulo de mesmo número de grupos.
- Janela da passada 3 (5/6) para três pontos por peça no estudo do estilo interno, se houver.
- Checar se os compositores mais compactos têm arquivos MIDI mais homogêneos (duração, polifonia).
