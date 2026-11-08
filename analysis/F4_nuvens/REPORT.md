# F4 — Ponto contra nuvem (Q2)

## Pergunta
Quanto da variação entre peças é explicado pelo compositor? O estilo é um ponto ou uma nuvem?

## Hipótese registrada
- **H3:** o compositor explica uma minoria da variância entre peças (o estilo é mais nuvem que ponto).
- **H4:** o gênero da peça rivaliza com o compositor na organização local.

## Configuração
- Camada 6, pooling média, nível de peça (2.183 peças, 52 compositores), espaço centrado, norma 1.
- Variância explicada: R² multivariado (traço entre / traço total). Nulo: 200 permutações de rótulos.
- Dispersão por compositor com n igualado: 200 sorteios de 20 peças.
- Sobreposição: fração das peças mais perto do centróide de outro compositor (o centróide próprio é recalculado sem a peça).
- Gênero (H4): palavra-chave no título, 16 gêneros. Só 1.053 peças têm gênero; as demais ficam como "outro" e saem.
- Obras atípicas: z da distância da peça ao próprio centróide, dentro do compositor.

## Resultado
- **H3:** R² do compositor = 0,230. Nulo: média 0,0235, p95 0,0254.
- **Sobreposição:** 68,8% das peças ficam mais perto do centróide de outro compositor. Em `acerto_centroide.csv`, o acerto médio por compositor é 0,314.
  - Acerto de 1,00 em Victoria, 0,97 em Meyer-Helmund, 0,88 em C. L. Johnson, 0,80 em J. Scott, 0,77 em Joplin.
  - Acerto de 0 em Brahms, Busoni, Ravina, Schumann e Tchaikovsky, entre outros.
- **H4** (1.053 peças com gênero):
  - R² do gênero = 0,133; R² do compositor nas mesmas peças = 0,269.
  - Distância média entre peças: mesmo compositor e mesmo gênero 0,689; mesmo compositor e gênero diferente 0,817; mesmo gênero e compositor diferente 0,965; tudo diferente 1,014.
- **Dispersão (n = 20):** mais compactos Victoria (0,098), C. L. Johnson (0,287), J. Scott (0,325), Meyer-Helmund (0,332), Joplin (0,480). Mais espalhados Schubert (0,899), Schumann (0,902), Tchaikovsky (0,903), Busoni (0,906), Heller (0,914).
- **Atípicas:** a mais atípica é "Wedding of the Fairies Waltz" de Johnson (z = 4,45, mais perto de Nazareth). Segue a Fantasia em sol menor BWV 920 de Bach (z = 3,85, mais perto de Debussy).

## Comparação com o nulo
- R² do compositor (0,230) é cerca de 10 vezes o nulo (0,0235) e fica muito acima do p95 do nulo (0,0254).
- H4 não tem nulo próprio.

## O que não se pode concluir
- H3: o compositor explica 23% da variância. "Minoria" vale, e o efeito é real contra o nulo. Mas 77% restante inclui gênero, forma, tonalidade e ruído de transcrição, sem decomposição aqui.
- Os 68,8% não significam que o compositor não é identificável. O acerto de 31% é muito maior que o acaso de cerca de 1,9% (1/52). Mostram que a nuvem de um compositor se sobrepõe às de outros.
- H4 "não se confirma": o compositor pesa mais que o gênero (0,269 contra 0,133; 0,817 contra 0,965 nas distâncias). Cuidados:
  - o R² cresce com o número de grupos (52 compositores contra 16 gêneros) e não foi ajustado; as distâncias não têm esse problema;
  - o gênero vem de palavra-chave no título e só cobre 1.053 das 2.183 peças;
  - não há intervalo de confiança.
- Compacto não quer dizer estilo coeso. Victoria tem exatamente 20 peças, e não se sabe se a compacidade vem da música ou do tipo de arquivo MIDI. Isso não foi testado.
- A dispersão depende do n igualado em 20. Outro n pode mudar a ordem.
- As obras atípicas são para leitura qualitativa. Não foram verificadas à mão.

## Figuras
- [Dispersão por compositor](figs/dispersao.png)

## Ideias fora do escopo
- Direções de desvio por compositor; gênero contra compositor com modelo misto (previstos como "depois").
- IC bootstrap para o R² e para o R² do gênero, com nulo de mesmo número de grupos.
- Checar se os compositores mais compactos têm arquivos MIDI mais homogêneos (duração, polifonia).
