# F3 — Geometria do mapa (Q1)

## Pergunta
Quem fica perto de quem? A proximidade acompanha período e nacionalidade?

## Hipótese registrada
- **H1:** a distância entre centróides cresce com a diferença de época (Mantel positivo, acima do nulo).
- **H2:** o efeito da nacionalidade é menor e pode sumir ao controlar o período.

## Configuração
- Representação da F2: camada 6, pooling média. 52 compositores, 2.183 peças.
- Centróide = média das peças (espaço centrado, norma 1). Distância = cosseno.
- Intervalos das distâncias: bootstrap por peças, 200 repetições (colunas `ic_lo`, `ic_hi` em `afinidades.csv`).
- Mantel (Spearman) com |Δ ano de nascimento| e com "mesma nacionalidade", 5.000 permutações. Parcial: resíduo da distância sobre Δ ano.
- PCA dos centróides (SVD), só para ilustrar. Tico-Tico (Abreu) projetado como ilustração.
- Nascimento e nacionalidade vêm de `metadata_curated.csv` (conhecimento geral, marcado "verificar").

## Resultado
- **H1:** Mantel ρ = 0,485, p = 0,0002.
- **H2:** nacionalidade ρ = 0,082 (p = 0,019); controlando o período, ρ = 0,041 (p = 0,111).
- Distância média entre centróides: 0,942.
- PCA: PC1 explica 31,8% e PC2 20,5% da variância dos centróides. Correlação de Spearman entre distâncias originais e projetadas: 0,72.
- Vizinho mais próximo (`vizinhos.csv`), com IC bootstrap de `afinidades.csv`:
  - Haydn ↔ Mozart: 0,106 [0,094; 0,229]
  - Bach ↔ Handel: 0,193 [0,143; 0,278]
  - Debussy ↔ C. Scott: 0,162 [0,145; 0,452]
  - J. Scott ↔ C. L. Johnson: 0,082 [0,073; 0,129]
  - Joplin → J. Scott: 0,141 [0,111; 0,229]
  - Satie ↔ Rebikov: 0,282 [0,223; 0,460]
  - Medtner ↔ Schumann: 0,248 [0,260; 0,588] (a estimativa pontual fica fora do próprio intervalo, o que indica que o IC bootstrap não é confiável para este par)
  - Chopin → Scriabin: 0,358 [0,263; 0,521]. A relação não é mútua: o vizinho de Scriabin é Balakirev.
- Tico-Tico (uma peça): vizinhos C. L. Johnson (0,418), J. Scott (0,449), Nazareth (0,546), Wachs (0,555), Scarlatti (0,555).
- Calculado a partir dos centróides em `figuras_apresentacao.py` (não está no `metrics.json`): Spearman entre PC1 e ano de nascimento = 0,53; entre PC2 e ano = 0,27. O sinal do PC1 foi invertido na figura de apresentação para o tempo crescer para a direita.

## Comparação com o nulo
- Mantel: o p vem de permutar a ordem dos compositores nas matrizes. Com 5.000 permutações, 0,0002 é o menor p possível (1/5001).
- Nacionalidade: ρ pequeno, p = 0,019 sem controle. Com o período controlado, não passa de 0,05. Coerente com H2.
- Os vizinhos não têm nulo próprio. Só os IC de bootstrap.

## O que não se pode concluir
- H1 está confirmada, mas ρ = 0,48 é moderado. O ano de nascimento não explica a maior parte da ordem das distâncias.
- H2: "some ao controlar a época" vale para o teste parcial (p = 0,11). Não é prova de ausência de efeito.
- O mapa 2D distorce (ρ = 0,72). Distâncias no desenho não são as distâncias reais. PC1 acompanha a cronologia só em parte (ρ = 0,53).
- Os IC de vários pares são largos (ex.: Debussy ↔ C. Scott vai de 0,145 a 0,452). "Vizinho mais próximo" pode mudar com outra amostra de peças.
- Nacionalidade e nascimento foram curados à mão e não verificados em fonte externa.
- O Tico-Tico é uma peça só. Vizinhança de uma peça não é estilo de um compositor.
- A lista de "afinidades inesperadas" (`afinidades.csv`, resíduo linear) é dominada por Victoria (300 anos de distância). Não usar como achado; usar a lista de vizinhos.
- Uma distância pequena não diz por que dois compositores se parecem (harmonia, textura, gênero, forma do arquivo MIDI). Ver F4.

## Figuras
- [Mapa PCA](figs/mapa_pca.png)
- [Mapa para apresentação](figs/mapa_apresentacao.png)
- [Distância × diferença de época](figs/dist_vs_epoca.png)

## Ideias fora do escopo
- Mantel parcial de nacionalidade com mais controles; UMAP (já previstos como "depois").
- Refazer com as janelas das passadas 2 e 3 para estreitar os IC.
- Conferir os metadados curados em fonte externa.
