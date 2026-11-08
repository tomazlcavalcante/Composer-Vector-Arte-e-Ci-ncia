# F4 — Ponto contra nuvem (Q2)

Base sem duplicatas (08/11): números atualizados; conclusões inalteradas.

## Pergunta
Quanto da variação entre peças é explicado pelo compositor? O estilo é um ponto ou uma nuvem?

## Hipótese registrada
- **H3:** o compositor explica uma minoria da variância entre peças (o estilo é mais nuvem que ponto).
- **H4:** o gênero da peça rivaliza com o compositor na organização local.

## Configuração
- Camada 6, pooling média, nível de peça (2.103 peças, 52 compositores; cada peça é a média de 2 janelas, passada 2, números finais do ensaio), espaço centrado, norma 1.
- Variância explicada: R² multivariado (traço entre / traço total). Nulo: 200 permutações de rótulos.
- Dispersão por compositor com n igualado: 200 sorteios de 20 peças.
- Sobreposição: fração das peças mais perto do centróide de outro compositor (o centróide próprio é recalculado sem a peça).
- Gênero (H4): palavra-chave no título, 16 gêneros. Só 1.000 peças têm gênero; as demais ficam como "outro" e saem.
- Obras atípicas: z da distância da peça ao próprio centróide, dentro do compositor.

## Resultado
- **H3:** R² do compositor = 0,268. Nulo: média 0,0243, p95 0,0267.
- **Sobreposição:** 66,9% das peças ficam mais perto do centróide de outro compositor. Em `acerto_centroide.csv`, o acerto médio por compositor é 0,337.
  - Acerto de 1,00 em Victoria, 0,83 em Meyer-Helmund (só 6 peças), 0,81 em C. L. Johnson, 0,75 em Hitz e em J. Scott, 0,74 em Joplin.
  - Acerto de 0 em Lack; Ravina (0,04), Schumann (0,03), Villa-Lobos e Busoni (0,05) quase nunca acertam.
- **H4** (1.053 peças com gênero):
  - R² do gênero = 0,155; R² do compositor nas mesmas peças = 0,303.
  - Distância média entre peças: mesmo compositor e mesmo gênero 0,648; mesmo compositor e gênero diferente 0,779; mesmo gênero e compositor diferente 0,944; tudo diferente 1,017.
- **Dispersão (n = 20):** mais compactos Victoria (0,084), C. L. Johnson (0,251), J. Scott (0,297), Meyer-Helmund (0,318), Joplin (0,423). Meyer-Helmund tem agora só 6 peças (o resto eram cópias), reamostradas com reposição até 20 em cada sorteio, então o valor dele pesa menos. Mais espalhados Heller (0,902), Ravina (0,894), Gurlitt (0,884), Mendelssohn (0,876), Hummel (0,8745). Moszkowski (0,8675) e Schubert (0,8665) ficam logo atrás.
- **Atípicas** (`obras_atipicas.csv`): a mais atípica continua sendo "Wedding of the Fairies Waltz" de Johnson (z = 4,47, mais perto de Nazareth). Seguem "Solace" de Joplin (z = 4,25, mais perto de Rebikov) e a Fuga em lá menor B.144 de Chopin (z = 3,66, mais perto de Raff).
- **Passada 1 (1 janela, base com cópias), para comparar:** R² do compositor 0,230; sobreposição 68,8%; H4 com R² do gênero 0,133 e do compositor nas mesmas peças 0,269. Os mais compactos são os mesmos cinco (Victoria, Johnson, Meyer-Helmund, J. Scott, Joplin). Os mais espalhados mudaram em parte (antes Schubert, Schumann, Tchaikovsky, Busoni, Heller; agora só Heller se mantém, e a lista mudou de novo entre a base com e sem cópias), então a ordem dos espalhados é menos estável que a dos compactos. As conclusões de H3 e H4 não mudaram.

## Comparação com o nulo
- R² do compositor (0,268) é mais de 11 vezes o nulo (0,0243) e fica muito acima do p95 do nulo (0,0267).
- H4 não tem nulo próprio.

## O que não se pode concluir
- H3: o compositor explica 27% da variância. "Minoria" vale, e o efeito é real contra o nulo. Mas os 72% restantes inclui gênero, forma, tonalidade e ruído de transcrição, sem decomposição aqui.
- Os 66,9% não significam que o compositor não é identificável. A sonda (acurácia balanceada, 31%) e o acerto médio por centróide (34%) são muito maiores que o acaso de cerca de 1,9% (1/52). Mostram que a nuvem de um compositor se sobrepõe às de outros.
- H4 "não se confirma": o compositor pesa mais que o gênero (0,303 contra 0,155; 0,779 contra 0,944 nas distâncias). Cuidados:
  - o R² cresce com o número de grupos (52 compositores contra 16 gêneros) e não foi ajustado; as distâncias não têm esse problema;
  - o gênero vem de palavra-chave no título e só cobre 1.000 das 2.103 peças;
  - não há intervalo de confiança.
- Compacto não quer dizer estilo coeso. Victoria tem exatamente 20 peças, Meyer-Helmund só 6 (reamostradas com reposição), e não se sabe se a compacidade vem da música ou do tipo de arquivo MIDI. Isso não foi testado.
- A dispersão depende do n igualado em 20. Outro n pode mudar a ordem; entre as passadas 1 e 2 e depois da remoção das cópias, a lista dos espalhados já mudou.
- As obras atípicas são para leitura qualitativa. Não foram verificadas à mão.

## Estilo interno da obra (Meyer)
Pergunta: quanto do "estilo" já está dentro de uma única obra? Análise `intra_obra.py` → `metrics_intra_obra.json`, com as peças que têm 2 janelas (a do meio e a de 1/6; todas as 2.103), camada 6, média, espaço centrado, cosseno.

| distância cosseno média | valor |
|---|---|
| entre janelas da mesma peça | 0,438 |
| entre peças diferentes do mesmo compositor | 0,794 |
| entre compositores diferentes | 1,005 |

- Variância entre janelas explicada pela peça: R² bruto = 0,781. Explicada pelo compositor: R² bruto = 0,218.
- **Nulo por construção:** com apenas 2 janelas por peça, rótulos de pares aleatórios já dão R² ≈ (G−1)/(N−1) ≈ 0,50 (2.102/4.205 = 0,4999; o valor simulado de 0,4997 é da base anterior). Corrigido pelo acaso, (0,7809 − 0,50)/(1 − 0,50), o R² por peça é 0,56. Para o compositor por janela o nulo é ≈ 0,013 (permutado: 0,0127, valor da base anterior, que não está nos arquivos atuais e não foi recalculado), e o corrigido é (0,2175 − 0,013)/(1 − 0,013) = 0,207. Os dois R² brutos têm números de grupos muito diferentes (cerca de 2.103 peças contra 52 compositores) e não são comparáveis; não se deve ler "78% contra 22%" como a peça pesar 3,5 vezes mais.
- Conferência no nível de peça com 2 janelas: R² do compositor = 0,268 (é o número de H3 acima).

**Leitura (cautelosa):**
- Duas janelas da mesma obra ficam bem mais perto uma da outra (0,44) do que duas obras do mesmo compositor (0,79), e estas só um pouco mais perto do que obras de compositores diferentes (1,01). O resultado mais robusto é a comparação direta: em 52 de 52 compositores, as janelas da mesma peça ficam mais próximas entre si do que de outras peças do mesmo compositor (diferença 0,33, IC95% 0,30–0,36). O R² bruto de 0,78 deve ser lido contra o nulo de ~0,50 do desenho de 2 janelas (corrigido: 0,56). O compositor aparece como um agrupamento mais frouxo das peças. Esse padrão é confundido com a gravação e o arquivo MIDI, que são os mesmos nas duas janelas.
- Isso é coerente com a imagem de "nuvem" de H3: parte da dispersão do compositor é variação entre obras, não ruído dentro delas.
- Limites: o R² por peça se apoia em só 2 janelas por peça (nulo de ~0,50 por construção, acima) e não tem IC. As duas janelas de uma peça compartilham tonalidade, textura, andamento e o arquivo MIDI, então "identidade da obra" mistura estilo da obra com características do arquivo; isso não foi separado. O R² do compositor entre janelas (0,218) e entre peças (0,268) têm unidades diferentes (janela contra média de 2 janelas) e não devem ser lidos como a mesma quantidade.
- Não é uma medida direta do "estilo interno" no sentido musical de Meyer (expectativas dentro da obra), e sim da variação do vetor do modelo entre trechos de uma mesma peça.

## Figuras
- [Dispersão por compositor](figs/dispersao.png)

## Ideias fora do escopo
- Direções de desvio por compositor; gênero contra compositor com modelo misto (previstos como "depois").
- IC bootstrap para o R² e para o R² do gênero, com nulo de mesmo número de grupos.
- Janela da passada 3 (5/6) para três pontos por peça no estudo do estilo interno, se houver.
- Checar se os compositores mais compactos têm arquivos MIDI mais homogêneos (duração, polifonia).
