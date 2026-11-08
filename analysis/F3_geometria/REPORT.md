# F3 — Geometria do mapa (Q1)

Base sem duplicatas (08/11): números atualizados; conclusões inalteradas.

## Pergunta
Quem fica perto de quem? A proximidade acompanha período e nacionalidade?

## Hipótese registrada
- **H1:** a distância entre centróides cresce com a diferença de época (Mantel positivo, acima do nulo).
- **H2:** o efeito da nacionalidade é menor e pode sumir ao controlar o período.

## Configuração
- Representação da F2: camada 6, pooling média. 52 compositores, 2.103 peças (sem as 80 cópias), cada uma a média de 2 janelas (passada 2; números finais do ensaio).
- Centróide = média das peças (espaço centrado, norma 1). Distância = cosseno.
- Intervalos das distâncias: bootstrap por peças, 200 repetições (colunas `ic_lo`, `ic_hi` em `afinidades.csv`).
- Mantel (Spearman) com |Δ ano de nascimento| e com "mesma nacionalidade", 5.000 permutações. Parcial: resíduo da distância sobre Δ ano.
- PCA dos centróides (SVD), só para ilustrar. Tico-Tico (Abreu) projetado como ilustração.
- Nascimento e nacionalidade vêm de `metadata_curated.csv` (conhecimento geral, marcado "verificar").

## Resultado
- **H1:** Mantel ρ = 0,502, p = 0,0002.
- **H2:** nacionalidade ρ = 0,082 (p = 0,020); controlando o período, ρ = 0,040 (p = 0,116).
- Distância média entre centróides: 0,931.
- PCA: PC1 explica 33,8% e PC2 19,3% da variância dos centróides. Correlação de Spearman entre distâncias originais e projetadas: 0,75.
- **Passada 1 (1 janela, base com cópias), para comparar:** Mantel ρ = 0,485; nacionalidade ρ = 0,082 (parcial 0,041, p = 0,111); distorção da PCA 0,72; distância média 0,942. As conclusões de H1 e H2 não mudaram.
- Vizinho mais próximo (`vizinhos.csv`), com IC bootstrap de `afinidades.csv`:
  - Haydn ↔ Mozart: 0,107 [0,087; 0,213]
  - Bach ↔ Handel: 0,175 [0,122; 0,288]. Agora é mútuo (sem as cópias de Handel); o segundo vizinho de Bach é Scarlatti (0,202 [0,165; 0,257]).
  - Debussy → C. Scott: 0,172 [0,126; 0,425]. Não é mais mútuo: o vizinho de C. Scott é Turina (0,164 [0,155; 0,321]).
  - J. Scott ↔ C. L. Johnson: 0,075 [0,063; 0,113]
  - Joplin → J. Scott: 0,133 [0,083; 0,218]
  - Satie → Rebikov: 0,289 [0,208; 0,458]. Não é mútuo: o vizinho de Rebikov é Scharwenka (0,278).
  - Medtner → Rachmaninoff: 0,233 [0,195; 0,492]. Medtner–Schumann (0,239 [0,224; 0,485]) deixou de ser o par mais próximo (o vizinho de Schumann ainda é Medtner).
  - Chopin ↔ Grieg: 0,319 [0,266; 0,597]. Agora é mútuo. Na passada 1 o vizinho de Chopin era Scriabin, que agora está a 0,329 [0,253; 0,491] de Chopin; o vizinho de Scriabin é Balakirev (0,131).
- Tico-Tico (uma peça): vizinhos C. L. Johnson (0,417), J. Scott (0,444), Nazareth (0,489), Czerny (0,499), Wachs (0,511). Passada 1: os três primeiros iguais; 4º e 5º eram Wachs e Scarlatti.
- Calculado a partir dos centróides em `figuras_apresentacao.py` (não está no `metrics.json`; valor registrado no DIARIO para 2 janelas): Spearman entre PC1 e ano de nascimento = 0,499 (`F11_tempo/metrics.json`, base sem cópias; era 0,525 na base anterior). O sinal do PC1 foi invertido na figura de apresentação para o tempo crescer para a direita. O PC2 × ano não foi recalculado (era 0,26 na base anterior).

## Comparação com o nulo
- Mantel: o p vem de permutar a ordem dos compositores nas matrizes. Com 5.000 permutações, 0,0002 é o menor p possível (1/5001).
- Nacionalidade: ρ pequeno, p = 0,019 sem controle. Com o período controlado, não passa de 0,05. Coerente com H2.
- Os vizinhos não têm nulo próprio. Só os IC de bootstrap.

## O que não se pode concluir
- H1 está confirmada, mas ρ = 0,50 é moderado. O ano de nascimento não explica a maior parte da ordem das distâncias.
- H2: "some ao controlar a época" vale para o teste parcial (p = 0,12). Não é prova de ausência de efeito.
- O mapa 2D distorce (ρ = 0,75). Distâncias no desenho não são as distâncias reais. Por isso o título da figura de apresentação diz que o eixo principal "acompanha, em parte, a cronologia" (PC1 × ano de nascimento, ρ = 0,499): há relação com o tempo, mas não é uma linha do tempo.
- Os IC de vários pares são largos (ex.: Debussy → C. Scott vai de 0,126 a 0,425; Chopin ↔ Grieg, de 0,266 a 0,597). "Vizinho mais próximo" pode mudar com outra amostra de peças.
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
