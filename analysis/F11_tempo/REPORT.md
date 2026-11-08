# F11 — À frente ou atrás do seu tempo? (C1)

## Pergunta
Dado o ano de nascimento, quais compositores o modelo posiciona mais "à frente" ou mais "atrás" no eixo principal (PC1) do mapa?

## Hipótese registrada
Exploratória (sem H numerada). Só se reportam resíduos com IC95% que exclui zero.

## Configuração
- Base sem controle de gênero: camada 6, média, janelas 1 e 2; 52 compositores, 2.183 peças. PCA dos centróides como em F3; PC1 orientado para crescer com o nascimento.
- Reta PC1 ~ nascimento (mínimos quadrados) e resíduo por compositor.
- IC95% por bootstrap de peças (1.000 reamostras): reamostram-se as peças de cada compositor, recalculam-se os centróides, projetam-se nos mesmos eixos (média e PC1 originais) e calcula-se o resíduo com a mesma reta.

## Resultado
- PC1 explica 33,5% da variância dos centróides. Spearman PC1 × nascimento = 0,52. R² da reta = 0,35.
- 37 dos 52 compositores têm IC que exclui zero (`residuos_tempo.csv`).
- **Soam mais modernos que a data (resíduo positivo, 19):** Victoria, Meyer-Helmund, Scharwenka, Fauré, Balakirev, Scriabin, Lange, Debussy, Chopin, C. Scott, Brahms, Godard, Liszt, Turina, Lack, Rachmaninoff, Grieg, Schumann, Rebikov (em ordem decrescente de resíduo; maiores: Victoria 0,46, Meyer-Helmund 0,41, Scharwenka 0,37).
- **Soam mais antigos que a data (resíduo negativo, 18):** Johnson (−0,68), J. Scott (−0,64), Joplin (−0,43), Haydn (−0,35), Beethoven (−0,30), Mozart (−0,29), Nazareth, Bach, Hummel, Scarlatti, Raff, Hitz, Czerny, Wachs, Gurlitt, Satie, Handel, Rzewski (−0,10).
- Sem resíduo distinguível de zero: Medtner, Ravina, Gottschalk, Heller, Chaminade, Teilman, Busoni, Schubert, Mendelssohn, Moszkowski, Prokofiev, Alkan, Villa-Lobos, Tchaikovsky, Poulenc.
- Padrão: o ragtime (Joplin, J. Scott, Johnson, Nazareth) cai muito abaixo da reta, o que é esperado de um modelo treinado em música popular que reconhece o idioma de dança dos anos 1900 como "antigo" no eixo; o Classicismo fica abaixo e o Romantismo médio-tardio acima.

## Comparação com o nulo
Não há nulo permutado. O IC mede apenas a variação por amostragem das peças; não inclui a incerteza da própria reta nem dos eixos da PCA (fixos na versão original). Por isso 37 de 52 serem "significativos" não indica 37 casos notáveis: a reta é uma aproximação grosseira (R² = 0,35) e um desvio sistemático de grupo (ex.: toda a música do Classicismo) produz resíduos significativos em bloco.

## O que não se pode concluir
- Isso é posição no espaço do modelo, não juízo histórico: "mais moderno que a data" não significa que a música seja de fato inovadora, só que seu centróide fica numa região do PC1 típica de nascidos mais tarde.
- O PC1 explica cerca de 34% da variância dos centróides; os outros 66% não entram. O mapa 2D tem distorção (Spearman 0,76 entre distâncias originais e projetadas, F3).
- A relação PC1 × nascimento é monotônica, não linear; um ajuste linear gera resíduos de sinal sistemático nos extremos. Victoria (nascido em 1548, único renascentista) tem alavancagem sobre a reta e seu resíduo positivo grande é em parte efeito de extrapolação.
- Nascimento é só um proxy da época do estilo (Beethoven é nascido em 1770 mas escreve até 1827; Hummel, Czerny e Raff são mais conservadores que sua data).
- Peças por compositor variam muito (ICs largos para n pequeno).
- O repertório é uma amostra (piano, bases públicas), não a obra completa.

## Figuras
- `figs/tempo_vs_mapa.png`: nascimento × PC1, reta, rótulos únicos (J. Scott e C. Scott distintos), barras de IC e contorno preto nos significativos, cor por período (paleta de F3).

## Ideias fora do escopo
- Ajuste não linear (spline) ou robusto; bootstrap que reajusta a reta e a PCA em cada reamostra.
- Repetir com os resíduos de gênero (F10) para ver se o ragtime continua abaixo da reta.
