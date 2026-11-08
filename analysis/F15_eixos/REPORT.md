# F15 — O que o eixo do tempo do mapa "ouve" (H17)

## Hipótese registrada (antes dos resultados)

- **PC1** (eixo cronológico; orientado pelo nascimento, como em `D1_explorador/export.py`) correlaciona **positivamente** com `entropia_pc` (cromatismo), `polifonia_media` e `extensao`.
- **PC2** correlaciona com `notas_por_s` (positivo) e com o **inverso da variabilidade rítmica**. Não há descritor de regularidade rítmica em `DESCRITORES.md`; uso como **aproximação** `ioi_mediano_s` (esperado ρ < 0: ritmo rápido, intervalo curto entre ataques) e `frac_acordes` (esperado ρ > 0: escrita em blocos/acompanhamento regular). Essa escolha de sinais é minha interpretação, fixada antes de ver os números. Nenhum dos dois mede variabilidade de fato.
- Critério: confirmada se o sinal esperado aparece no nível de compositor com p de permutação unicaudal < 0,05. O sinal do PC2 é arbitrário (SVD); só vale a coerência entre os sinais esperados.

## Método

Camada 6, pooling mean, janelas 1 e 2, 2.103 peças, 52 compositores (sem duplicatas). PCA dos centróides (PC1 34%, PC2 19% da variância); as peças são projetadas nos mesmos eixos. Descritores por peça = média das janelas 1 e 2 de `descritores_janelas.csv` (casados por `piece_id`; nenhuma peça sem descritor). Spearman de PC1 e PC2 com cada descritor, por peça e por compositor (médias dos descritores das peças vs. posição do centróide). No nível de compositor, p por 10.000 permutações. Os p no nível de peça são ingênuos (as peças de um compositor não são independentes) e não devem ser lidos como evidência.

## Resultados (ρ de Spearman; compositor, p de permutação unicaudal na direção esperada)

| Eixo | Descritor | ρ peça | ρ compositor | p |
|---|---|---|---|---|
| PC1 | entropia_pc | 0,365 | 0,600 | < 0,001 |
| PC1 | polifonia_media | 0,844 | 0,849 | < 0,001 |
| PC1 | extensao | 0,293 | 0,432 | 0,001 |
| PC2 | notas_por_s | 0,665 | 0,665 | < 0,001 |
| PC2 | ioi_mediano_s (aprox.) | −0,360 | −0,381 | 0,003 |
| PC2 | frac_acordes (aprox.) | 0,724 | 0,652 | < 0,001 |

Os outros descritores estão em `correlacoes.csv` e na figura `figs/eixos_descritores.png`. Pontos que não estavam na hipótese:
- A maior correlação do PC1 é com **duracao_media_s** (ρ compositor 0,846), tão alta quanto a polifonia; as duas são provavelmente redundantes entre si (notas longas sustentadas empilham notas soando juntas). Não separei as duas.
- PC1 tem correlação negativa fraca com notas_por_s (−0,24) e com frac_acordes (−0,27), com p bicaudal entre 0,05 e 0,09 no nível de compositor.
- O PC2 também correlaciona com intervalo_melodico_medio (0,61), altura_dp (0,50) e extensao (0,45): é um eixo de "movimento/agitação", não só de notas por segundo.

## Veredito H17

**Confirmada nos sinais registrados**, para PC1 (as três correlações são positivas) e para PC2 (notas_por_s positivo; as duas aproximações de regularidade com os sinais esperados). Com ressalvas: a hipótese ficou aquém do que os dados mostram, pois polifonia e duração média dominam o PC1 e o cromatismo é a mais fraca das três. A parte do PC2 sobre "variabilidade rítmica" só foi testada por proxies que não medem variabilidade.

## Cautelas

- Correlação não é mecanismo: que o PC1 acompanhe a polifonia e a duração não mostra que o modelo "usa" esses descritores; a mesma estrutura pode vir de gênero, instrumento (piano vs. outros), gravação ou arquivo, todos confundidos com a época. A F9 já mostrou que os descritores sozinhos explicam só parte da variância das representações.
- Os descritores são simples, calculados em duas janelas de cada peça e sobre MIDI (de transcrição, no caso de parte da base), e correlacionam entre si.
- Spearman de centróides (n = 52) é sensível a poucos compositores influentes; sem IC por bootstrap de peças.
- O nível de peça tem n alto mas dependência forte dentro do compositor.
