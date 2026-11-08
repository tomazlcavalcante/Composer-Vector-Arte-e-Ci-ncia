# F8 — Expectativa e surpresa (ponte com Meyer)

## Pergunta
O quanto o modelo se surpreende (perda média por token) varia entre compositores e ao longo do tempo? Isso dialoga com a "expectativa" de Meyer, desde que lido com cuidado.

## Hipótese registrada
A surpresa do modelo não é uniforme entre compositores. Como o AMT foi treinado no Lakh (música popular e variada), espera-se surpresa menor para estilos mais próximos de tonalidade e ritmo regulares.

## Configuração
- Perda média por token (nats) de cada janela, campo `loss` dos npz. Só janelas 1 e 2 (4.366 janelas, 2.183 peças, 52 compositores com `incluir == 1`). A camada não influencia a perda.
- Surpresa da peça = média das 2 janelas. Por compositor: média das peças e IC95% por bootstrap de peças (1.000 reamostras, semente 0).
- Época: Spearman entre a surpresa média do compositor e o ano de nascimento (IC por bootstrap de compositores); Kruskal-Wallis entre períodos no nível de peça, com nulo extra permutando o período entre compositores (500 permutações), porque as peças de um mesmo compositor não são independentes.
- Controle: ver "O que não se pode concluir". Não há medida de densidade de notas nos arquivos, e nenhuma foi inventada.

## Resultado
- Surpresa média das peças: 2,49 nats/token (dp 0,48 entre peças; dp 0,31 entre compositores). Menor: Victoria 1,74. Maior: Scharwenka 3,32. Depois dele: Rzewski 3,22, Scriabin 3,17, Lack 3,16, Fauré 2,91.
- Mais previsíveis para o modelo (após Victoria): C. L. Johnson 1,94, Raff 1,94, J. Scott 2,08, Nazareth 2,20, Joplin 2,20, Handel 2,21. Bach 2,28, Scarlatti 2,25 e Beethoven 2,25 ficam abaixo da média.
- **Época:** Spearman compositor × nascimento ρ = 0,51 (IC95% 0,23–0,73; p = 1,2e-4; n = 52). No nível de peça, ρ = 0,34 (n = 2.183, p-valor inflado por dependência).
- **Períodos (peça):** Kruskal-Wallis H = 243 (p ≈ 2e-51), ε² = 0,11. Médias: Barroco 2,25 (3 compositores), Clássico 2,32 (4), Romântico 2,54 (33), Moderno 2,70 (11); Renascimento 1,74 é um único compositor (Victoria).
- O compositor explica η² = 0,37 da variância da surpresa entre peças.

## Comparação com o nulo
- η² do compositor: nulo de permutação de rótulos com média 0,024 e p95 0,032. O observado (0,37) está muito acima.
- Kruskal-Wallis permutando o período entre compositores: p = 0,008. O efeito de período sobrevive, mas é bem menos forte do que o p da peça sugere. Com 52 compositores efetivos, é a leitura a ser usada.
- Confiabilidade: Spearman janela 1 × janela 2 dentro da peça = 0,72; entre médias por compositor, 0,98. O ranking de compositores é estável com as duas janelas separadas.

## O que NÃO se pode concluir
- **Perda baixa significa "previsível PARA ESTE MODELO"**, isto é, para um modelo treinado no Lakh MIDI. Reflete o acervo de treino, não uma propriedade intrínseca da música. A surpresa do modelo não é a expectativa de um ouvinte, nem a de Meyer.
- **Controle de densidade de notas: não feito.** Os arquivos só têm `n_tokens`. Todas as janelas têm 1.024 tokens, exceto algumas curtas (mínimo 241, mediana 1.024), então ele não mede densidade. Densidade, tessitura, textura e repetição literal podem explicar parte da surpresa. O que temos é só a variância dentro do compositor: o desvio entre peças (mediana 0,36 por compositor) é 1,14 vez o desvio entre compositores (0,31), e o coeficiente de variação intra mediano é 0,14. Ou seja, a variação intra é grande e o compositor é só parte do quadro (η² = 0,37).
- A hipótese ("tonalidade e ritmo regulares") **não foi testada diretamente**: não medimos regularidade. Os mais previsíveis incluem ragtime e maxixe (Johnson, Scott, Joplin, Nazareth) e barrocos, compatíveis com a hipótese, mas também Raff e Victoria; e os mais surpreendentes (Scharwenka, Lack, Rzewski) não são um bloco estilístico óbvio. Compatibilidade não é teste.
- A tendência com a época é correlacional. Fica confundida com tamanho e tipo de acervo por período: Renascimento tem 1 compositor, Barroco 3, Clássico 4. Também pode refletir o quanto cada repertório aparece no Lakh, a transcrição (GiantMIDI vem de gravações transcritas automaticamente, com ruído que pode aumentar a surpresa) e o gênero da peça.
- Cada peça entra com 2 janelas, qualquer que seja o seu tamanho; peças longas e curtas têm o mesmo peso.

## Figuras
- `figs/surpresa_por_compositor.png`: surpresa média e IC95% por compositor, em ordem de nascimento, cor por período (mesma paleta da F3). Tabela em `surpresa_por_compositor.csv`; números em `metrics.json`.

## Ideias fora do escopo
- Medir regularidade com estatísticas simbólicas simples (entropia da duração e das classes de altura, densidade de notas por janela a partir dos MIDIs) e usar como covariáveis da surpresa. Só então testar a hipótese de tonalidade e ritmo regulares.
- Surpresa por posição dentro da janela (perda token a token), para ver onde o modelo erra mais.
- Comparar com um modelo treinado só em música de piano erudita, para separar "música surpreendente" de "música distante do treino".
- Surpresa no nível de gênero da peça, usando as palavras-chave do título da F4.
