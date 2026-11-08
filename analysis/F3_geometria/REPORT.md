# F3 — Geometria do mapa (Q1)

## Pergunta
Quem fica perto de quem? A proximidade acompanha período e nacionalidade?

## Hipótese registrada
- **H1:** a distância entre centróides cresce com a diferença de época (Mantel positivo, acima do nulo).
- **H2:** o efeito da nacionalidade é menor e pode sumir ao controlar o período.

## Configuração
- Representação da F2: camada 6, pooling média. 52 compositores, 2.183 peças, cada uma a média de 2 janelas (passada 2; números finais do ensaio).
- Centróide = média das peças (espaço centrado, norma 1). Distância = cosseno.
- Intervalos das distâncias: bootstrap por peças, 200 repetições (colunas `ic_lo`, `ic_hi` em `afinidades.csv`).
- Mantel (Spearman) com |Δ ano de nascimento| e com "mesma nacionalidade", 5.000 permutações. Parcial: resíduo da distância sobre Δ ano.
- PCA dos centróides (SVD), só para ilustrar. Tico-Tico (Abreu) projetado como ilustração.
- Nascimento e nacionalidade vêm de `metadata_curated.csv` (conhecimento geral, marcado "verificar").

## Resultado
- **H1:** Mantel ρ = 0,505, p = 0,0002.
- **H2:** nacionalidade ρ = 0,083 (p = 0,019); controlando o período, ρ = 0,041 (p = 0,111).
- Distância média entre centróides: 0,932.
- PCA: PC1 explica 33,5% e PC2 19,6% da variância dos centróides. Correlação de Spearman entre distâncias originais e projetadas: 0,76.
- **Passada 1 (1 janela), para comparar:** Mantel ρ = 0,485; nacionalidade ρ = 0,082 (parcial 0,041, p = 0,111); distorção da PCA 0,72; distância média 0,942. As conclusões de H1 e H2 não mudaram.
- Vizinho mais próximo (`vizinhos.csv`), com IC bootstrap de `afinidades.csv`:
  - Haydn ↔ Mozart: 0,101 [0,082; 0,186]
  - Bach ↔ Handel: 0,209 [0,159; 0,302]. Handel tem Bach como vizinho mais próximo, mas o vizinho de Bach passou a ser Scarlatti (0,200 [0,160; 0,260]).
  - Debussy ↔ C. Scott: 0,157 [0,123; 0,385]
  - J. Scott ↔ C. L. Johnson: 0,075 [0,066; 0,117]
  - Joplin → J. Scott: 0,133 [0,100; 0,212]
  - Satie → Rebikov: 0,284 [0,221; 0,456]. Não é mútuo: o vizinho de Rebikov é Scharwenka (0,267).
  - Medtner ↔ Schumann: 0,236 [0,210; 0,508]
  - Chopin → Grieg: 0,322 [0,249; 0,614]. Na passada 1 o vizinho de Chopin era Scriabin; agora Scriabin está a 0,336 [0,244; 0,490] de Chopin, e o vizinho de Scriabin é Balakirev (0,136). Nenhuma das duas relações com Chopin é mútua (o vizinho de Grieg é Chopin; o de Scriabin é Balakirev).
- Tico-Tico (uma peça): vizinhos C. L. Johnson (0,417), J. Scott (0,444), Nazareth (0,488), Czerny (0,540), Joplin (0,541). Passada 1: os três primeiros iguais; 4º e 5º eram Wachs e Scarlatti.
- Calculado a partir dos centróides em `figuras_apresentacao.py` (não está no `metrics.json`; valor registrado no DIARIO para 2 janelas): Spearman entre PC1 e ano de nascimento = 0,525 (recalculado pela revisão independente; PC2 × ano = 0,26). O sinal do PC1 foi invertido na figura de apresentação para o tempo crescer para a direita. O PC2 não foi recalculado para este REPORT.

## Comparação com o nulo
- Mantel: o p vem de permutar a ordem dos compositores nas matrizes. Com 5.000 permutações, 0,0002 é o menor p possível (1/5001).
- Nacionalidade: ρ pequeno, p = 0,019 sem controle. Com o período controlado, não passa de 0,05. Coerente com H2.
- Os vizinhos não têm nulo próprio. Só os IC de bootstrap.

## O que não se pode concluir
- H1 está confirmada, mas ρ = 0,50 é moderado. O ano de nascimento não explica a maior parte da ordem das distâncias.
- H2: "some ao controlar a época" vale para o teste parcial (p = 0,11). Não é prova de ausência de efeito.
- O mapa 2D distorce (ρ = 0,76). Distâncias no desenho não são as distâncias reais. Por isso o título da figura de apresentação diz que o eixo principal "acompanha, em parte, a cronologia" (PC1 × ano de nascimento, ρ = 0,525): há relação com o tempo, mas não é uma linha do tempo.
- Os IC de vários pares são largos (ex.: Debussy ↔ C. Scott vai de 0,123 a 0,385; Chopin → Grieg, de 0,249 a 0,614). "Vizinho mais próximo" pode mudar com outra amostra de peças.
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
- Refazer com a janela da passada 3 (5/6) para estreitar os IC, se houver.
- Conferir os metadados curados em fonte externa.
