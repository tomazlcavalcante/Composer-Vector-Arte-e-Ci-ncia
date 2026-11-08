# Revisão independente (F2–F7, VALIDADE, DIARIO)

Método: cada número dos REPORTs, de VALIDADE.md e de DIARIO.md foi comparado com metrics*.json e CSV da pasta. Médias, erros padrão, contagens e Wilcoxon (exato) de F7 foram recalculados dos CSV. Fora isso, recalculei com os embeddings já extraídos (sem modelo): PC1 × nascimento e o nulo do R² por peça (item 2). Nada foi editado.

Resumo: F2, F3 (quase todo), F4, F5 e F7 batem com os arquivos. Os problemas reais são (a) REPORTs de F6 e F7 que usam base de 1 janela e F6 contradiz VALIDADE/DIARIO, (b) o R² "a peça explica 78%" sem nulo, que é em boa parte aritmético, (c) "Satie ↔ Rebikov" não é mútuo, (d) "12% das peças" e "9% das peças" são linhas, não peças, e (e) algumas redações interpretativas fortes.

## 1. Tabela de problemas

| arquivo | trecho | problema | valor correto / fonte | gravidade |
|---|---|---|---|---|
| F6/REPORT.md | Seção Passada 1 e todo o Resultado: n×distância −0,11; n×dispersão 0,004; refs 0,942 e 0,542; "12,2% (22 de 180)" | REPORT está na base da passada 1, mas `metrics.json` e `transposicao.csv` atuais são de 2 janelas (DIARIO 06:30 e VALIDADE dizem isso). O texto diz explicitamente que F6 "não foi refeita", o que hoje é falso. REPORT e VALIDADE se contradizem | `metrics.json`: n×dist −0,116; n×z 0,461; n×dispersão 0,043; muda centróide 0,094 (17 de 180); ref entre centróides 0,9315; ref peça-centróide 0,4938. Passada 1 está em `metrics_passada1.json` | alta |
| F6/REPORT.md | "4 a 5% da distância peça-centróide (0,542) e 2 a 3% da entre centróides (0,942)" | Percentuais derivam das referências antigas | Base atual: 0,022–0,027 / 0,494 = 4,5–5,4%; / 0,9315 = 2,4–2,9% | média |
| F6/REPORT.md e VALIDADE.md (cabeçalho, "Base: ... 2 janelas por peça") | Transposição "refeita com 2 janelas" | A transposição re-extrai só a janela do meio (`run.py` linha 80, `window(..., 0.5)`). Os deslocamentos são idênticos nas duas passadas (0,0223 e 0,0269; diferença máxima por linha 0,0008). Só as referências e o centróide mais próximo usam 2 janelas. Misturar vetor de 1 janela com centróides de 2 janelas não é o mesmo que transpor a peça de 2 janelas | `transposicao.csv` vs `transposicao_passada1.csv` | média |
| F6 (REPORT/VALIDADE linha 12) / DIARIO 22:40 | "12% das peças trocam de centróide" (DIARIO); "em 9% das peças transpostas (contando cada transposição)" (VALIDADE) | Contagem é de linhas (peça × transposição). Por peça: 13 de 45 (29%) trocam de centróide mais próximo em pelo menos uma transposição, nas duas bases. O DIARIO erra mais: chama de "peças". Além disso, 23 das 180 linhas mudam de resposta entre as duas bases (22 → 17 trocas), então 9% vs 12% não é um número estável | `transposicao.csv`: 17/180 linhas; 13/45 peças | média |
| F3/REPORT.md, VALIDADE linha 7, DIARIO 22:40 | "Satie ↔ Rebikov" (seta dupla) | Não é mútuo. O vizinho de Satie é Rebikov (0,284), mas o de Rebikov é Scharwenka (0,267). A seta ↔ está certa para Haydn–Mozart, Debussy–C. Scott, J. Scott–Johnson, Medtner–Schumann; errada para Satie–Rebikov | `vizinhos.csv` | média |
| F3/REPORT.md (PC1 × ano = 0,53); DIARIO 00:00 | "ρ = 0,53" | Recalculado com os embeddings (camada 6, média, 2 janelas, SVD dos centróides): ρ = 0,525 (0,52 se arredondar). PC2 × ano: 0,26. A variância explicada (33,5% e 19,6%) bate. Diferença é de arredondamento | recálculo próprio; o REPORT já diz que não está no `metrics.json` | baixa |
| F4/REPORT.md, seção Estilo interno | "Variância entre janelas explicada pela peça: R² = 0,783" e leitura "cada obra tem identidade própria forte" | R² sem nulo é enganoso. Com 2 janelas por grupo, agrupar por rótulos de pares aleatórios já dá R² ≈ 0,50 (analítico (G−1)/(N−1) = 0,4999; simulado 0,4997). O número informativo é 0,78 contra ~0,50, não contra 0. Do mesmo modo, o R² do compositor por janela (0,224) tem nulo ≈ 0,013 (permutado: 0,0127). O REPORT diz "sem nulo próprio", mas não avisa que o nulo é conhecido e alto | `metrics_intra_obra.json`; recálculo próprio | alta |
| F4/REPORT.md e DIARIO 00:00 | "A peça explica 78% da variância entre janelas, e o compositor 22%" | Mesma questão: os dois R² não são comparáveis, porque a peça tem ~2.183 grupos de 2 e o compositor 52 grupos. Mais grupos infla o R². Comparar 78% a 22% como "peça pesa 3,5 vezes mais" não vale | idem | alta |
| VALIDADE.md linha 1 | "Permutação (p = 0,001)" | F3 usa 5.000 permutações (p = 0,0002); `secundaria.py` usa 1.000 (p mínimo 0,001). Dois p diferentes para o mesmo H1 sem explicação | `metrics.json` F3: 0,0002; `metrics_secundaria.json`: 0,001 | baixa |
| VALIDADE.md linha 4 vs F4/REPORT | "H4 refutada" | O REPORT diz "não se confirma" e lista 3 cuidados (R² cresce com grupos, gênero por palavra-chave, 1.053 de 2.183 peças). "Refutada" é mais forte que o texto da F4 | F4/REPORT | baixa |
| VALIDADE.md linha 8 | Tico-Tico "estável entre 1 e 2 janelas" | Só os 3 primeiros vizinhos se mantêm. 4º e 5º mudam (Wachs, Scarlatti → Czerny, Joplin) e a distância a Nazareth vai de 0,546 para 0,488 | `metrics.json` vs `metrics_passada1.json` F3 | baixa |
| F7/REPORT.md, Configuração e (a) | Principal `steering_forte.csv` e caminho geométrico na base de 1 janela; varredura α e par inverso na de 2 janelas (uma das tabelas compara as duas lado a lado) | A tabela "Bach → Chopin (n = 14) × Chopin → Bach (n = 7)" compara, na coluna 1, centróides de 1 janela com, na coluna 2, 2 janelas. O REPORT admite a diferença só no parágrafo da varredura, não na tabela do par inverso. A "assimetria" (+0,292 vs +0,136) mistura eixo, base e n. Também usa 0,942 (1 janela) na mesma seção em que a varredura usa 2 janelas | `steering_forte.csv` vs `steering_alfa.csv`/`..._Chopin_Bach.csv`; DIARIO 00:00 | média |
| F7/REPORT.md | "A repetição de trigramas ficou ≤ 4% em todas as condições" | Média de "nenhum" é 4,14% (>4%). Por continuação, o máximo no forte é 28,9%; na varredura, 23,7%; no inverso, 39,5%. O DIARIO 00:40 diz "≤ 6% em tudo", mas aleatório α = 1,5 tem média 6,4% | `steering_forte.csv`, `steering_alfa.csv` | baixa |
| F7/REPORT.md | Mistura meio a meio "se comporta mais como o vetor de Bach" (DIARIO: "o vetor de Bach domina") | A norma NÃO é um confundidor (verificado em `run.py` linha 107: todo vetor é renormalizado para `hnorm`). Mas v = (1−t)v_B + t v_C com t = 0,5 muda a direção, e a direção resultante é a soma dos dois centrados; "Bach domina" é uma leitura causal sobre n = 14 (e 7 no inverso) com erro padrão 0,026–0,034, sem teste. t = 0,5 (0,338) fica abaixo de "nenhum" (0,392), diferença menor que 2 EP | tabelas do REPORT | baixa |
| DIARIO 06:30 | "as conclusões H1, H2, H3 e H5 não dependem da escolha fina da representação" | H1 (0,41–0,51) e H2 parcial (0,01–0,04) sim. H3 varia 0,12–0,28 e H5 muda de composição em camada 12 e último token (grupo de 12 e de 8 com intrusos). As 4 configurações usam os mesmos dados e as mesmas peças; só duas camadas e um pooling alternativo foram testados | `metrics_secundaria.json` | média |
| VALIDADE.md linha 12 | "O modelo separa estilo e não tonalidade" — **Sobrevive** | O teste mostra que deslocar o tom por ±2 ou ±5 mexe pouco no vetor da janela do meio (0,02–0,03), com 45 peças, uma janela, sem IC e sem nulo. 13 de 45 peças trocam de centróide mais próximo em alguma transposição. O F6/REPORT já diz que "não prova que o modelo ignora tonalidade". A linha da tabela diz o oposto do texto | `transposicao.csv`; F6/REPORT | média |
| VALIDADE.md linha 2 | "A nacionalidade não organiza o mapa quando a época é controlada" — **Sobrevive** | O teste parcial tem p = 0,12 com 52 compositores e metadados não verificados. É ausência de evidência, não evidência de ausência (o F3/REPORT diz isso; a VALIDADE não). Em outra configuração o ρ parcial vai de 0,01 a 0,04, sem IC | F3 `metrics.json` | média |
| F4/REPORT.md | Mais espalhados: "... Moszkowski (0,872), Mendelssohn (0,871)" | Correto, mas Schubert (0,8706, n = 96) fica a 0,0003 de Mendelssohn (0,8709, n = 24). A lista dos cinco depende de um empate | `dispersao.csv` | baixa |
| DIARIO 21:20 | "51 compositores ≥ 20 peças, 2.184 peças" | Os REPORTs usam 52 compositores e 2.183 peças. 2.184 inclui o Tico-Tico (Abreu, 1 peça); a contagem de 51 vs 52 não é explicada (metadata tem 52 com `incluir = 1`). Provavelmente o DIARIO descreve a decisão inicial | `metadata_curated.csv`; `load()` | baixa |

Conferido e sem problema (amostra do que foi checado): F2 inteira (tabela, somas 1,1831 vs 1,1826, passada 1: 0,301/0,791/0,190); F3 Mantel, nacionalidade, PCA, IC de todos os vizinhos, passada 1; F4 R², nulo, 11×, 65,3%, 0,346, acertos por compositor, H4, dispersão, atípicas, passada 1; F5 barras, razão, ARI, grupos nos cortes 2, 3 e 4 (25 e 16), passada 1; F7 todas as tabelas (médias, erros padrão, contagens por semente, p de Wilcoxon, distâncias a Chopin e Bach, ganho +0,292/+0,136/+0,251/+0,174, 15% e 87%, ρ = 0,53 com 42 compositores, distância ao segmento 0,288–0,947 média 0,477); VALIDADE linhas 1, 3, 5, 6, 9, 10, 11; DIARIO 22:40, 00:00 (exceto PC1), 00:40 (exceto "≤ 6%"), 06:30.

## 2. Afirmações interpretativas exageradas e redação sugerida

1. **F4b / DIARIO / VALIDADE linha 5: "cada obra tem identidade própria forte"; "a peça explica 78%".**
   Sugestão: "Duas janelas da mesma peça ficam mais próximas (cosseno 0,43) do que duas peças do mesmo compositor (0,79); isso vale em 52 de 52 compositores. O R² de 0,78 por peça deve ser lido contra o nulo de ~0,50 que o desenho de 2 janelas já impõe, e as janelas compartilham arquivo MIDI, gravação e tonalidade." Evitar comparar 78% com 22%.

2. **VALIDADE linha 12: "o modelo separa estilo e não tonalidade".**
   Sugestão: "Uma transposição de ±2 a ±5 semitons desloca o vetor da janela do meio em 0,02–0,03 (45 peças), pequeno diante de 0,49 (peça–centróide) e 0,93 (entre centróides). Em 13 de 45 peças o centróide mais próximo muda em alguma transposição. O teste não exclui que o mapa carregue tonalidade ou registro por outros caminhos."

3. **VALIDADE linha 2: nacionalidade "não organiza o mapa".**
   Sugestão: "Controlando a época, não detectamos associação com a nacionalidade (ρ parcial 0,04; p = 0,12; 52 compositores; nacionalidade curada sem verificação externa). O teste tem pouca potência."

4. **H6 "confirmada" (F7, DIARIO, VALIDADE linha 9).**
   O efeito é mensurado na mesma camada 6, no mesmo modelo, e o vetor centrado é construído com o mesmo centróide do alvo que define o eixo de progresso (o REPORT admite). Sugestão: "Somar o vetor centrado de Chopin na camada 6 aumenta a projeção da continuação, relida sem steering, no eixo Bach → Chopin em relação a um vetor aleatório de mesma norma (7 de 7 sementes de Bach, uma peça por semente, p = 0,016). Com α = 1,5 a distância ao centróide de Chopin cai de 1,18 para 0,85 e a distância a Bach sobe. Não houve avaliação por outra métrica, por outro par ou por escuta." Evitar "desloca a música em direção ao compositor" sem a parte "no eixo e no modelo usados".

5. **H7 "mistura meio a meio se comporta como Bach" / "o vetor de Bach domina".**
   Leitura causal, sem teste de diferença (a norma está controlada: todo vetor é renormalizado). Sugestão: "Com a mistura meio a meio (t = 0,5), o progresso (0,34; n = 14) fica perto do obtido com o vetor de Bach (0,28) e abaixo da continuação sem steering (0,39). Com um par e 7 sementes não dá para dizer se isso reflete dominância de Bach ou apenas de uma direção intermediária sem efeito distinguível."

6. **Assimetria Bach → Chopin vs. Chopin → Bach ("efeito cerca de metade no sentido inverso").**
   Eixos, sementes, base de centróides (1 vs 2 janelas) e n (14 vs 7) são diferentes; as continuações de Chopin sem steering repetem 12% dos trigramas contra 4%. Sugestão: "No sentido inverso o ganho foi menor (+0,14 contra +0,29); a comparação mistura eixos, sementes e bases e não permite atribuir a diferença ao vetor."

7. **"Monótono em α" (F7 varredura, DIARIO "H6 confirmada com 7 sementes").**
   A média sobe, mas só 4 de 7 sementes são monótonas, e há uma amostra por semente e por α. Sugestão: "A média do progresso cresce com α entre 0 e 1,5; por semente, a trajetória é monótona em 4 de 7."

8. **"Sem quebra até α = 1,5" (F7, DIARIO).**
   A única medida de degeneração é a repetição de trigramas (máximo 24% por continuação). Sugestão: "Não vimos aumento sistemático da repetição de trigramas até α = 1,5; isso não garante que a música seja coerente."

9. **F3: PC1 "acompanha, em parte, a cronologia" e H1 "confirmada".**
   Bem redigido. Manter, citando o ρ = 0,52–0,53 e que a figura inverte o sinal do PC1.

10. **F4/DIARIO: "o estilo é mais nuvem que ponto".**
    Metáfora apoiada em R² = 0,275 numa única representação (varia de 0,12 a 0,28 nas quatro testadas), com sobreposição de 65% pelo critério de centróide mais próximo, que é um classificador simples. Sugestão: "Nesta representação, o compositor explica 28% da variância entre peças (nulo 2%) e 65% das peças ficam mais perto do centróide de outro compositor."

11. **F5: "bloco pré-romântico é um ramo estável".**
    Estável no corte em 2 (ARI 0,78), mas é um grupo de 7 contra 45, e o teste da lacuna não rejeita o contínuo. Sugestão: "A ligação média separa de modo estável os sete compositores pré-românticos; o espaço, no resto, não mostra grupos além do esperado em uma nuvem gaussiana. Com 52 pontos o teste tem pouca potência."

12. **F3 vizinhos ("com sentido musical").**
    A interpretação "sentido musical" vem do conhecimento prévio do autor e muitos IC são largos (Chopin → Grieg [0,25; 0,61]). Já está tratada como ilustração na VALIDADE; manter.

13. **DIARIO 22:40 "só 12% das peças trocam de centróide mais próximo".**
    Sugestão: "Em 12% (1 janela; 9% com 2 janelas) das 180 combinações peça × transposição o centróide mais próximo muda."

## 3. O que está bem fundamentado

- Os números numéricos de F2, F3, F4, F5 e F7 reproduzem exatamente `metrics.json`, CSV e recálculos independentes de Wilcoxon, médias, erros padrão e contagens por semente.
- As seções "O que não se pode concluir" são honestas e, na maioria, já antecipam os problemas acima (único par de compositores, 7 sementes, 2 amostras não independentes, projeção ≠ chegar ao alvo, ordem dos vizinhos instável, falta de nulo para vizinhos, R² dependente do número de grupos em H4).
- A rastreabilidade entre passadas (`*_passada1.json`) está bem feita e os textos comparam as duas bases com os valores corretos.
- A comparação com nulo existe onde importa (Mantel com 5.000 permutações, R² com 200 permutações, barras H0 com 200 gaussianas, Wilcoxon contra vetor aleatório).
- A VALIDADE assinala corretamente o que nenhum controle cobre (pianista/gravação, modelo treinado em Lakh, poucos barrocos e clássicos).
