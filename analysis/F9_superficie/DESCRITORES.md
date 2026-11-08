# Descritores por janela (A1)

Calculados só a partir dos eventos MIDI da janela (sem o modelo). A janela é a mesma de `extract_amt.window` (k=1: meio; k=2: a 1/6). Tempo e duração em passos de 10 ms (TIME_OFFSET=0, DUR_OFFSET=MAX_TIME); altura = (tok - NOTE_OFFSET) % 128.
Arquivo: `/home/claude/data/descritores_janelas.csv` (ou .parquet), uma linha por (piece_id, window).

| coluna | significado |
|---|---|
| piece_id, composer_key, window | identificação (window 1 = meio, 2 = 1/6) |
| n_notas | notas na janela |
| span_s | do primeiro ataque ao fim da última nota (s) |
| notas_por_s | n_notas / span_s |
| altura_media, altura_dp | média e desvio-padrão da altura MIDI |
| extensao | percentil 95 menos percentil 5 da altura (semitons) |
| duracao_media_s | duração média das notas (s) |
| polifonia_media | média de notas soando, amostrando a cada 50 ms de 0 ao último ataque |
| ioi_mediano_s | mediana dos intervalos entre ataques distintos consecutivos (>0) (s) |
| frac_acordes | fração das notas cujo tempo de ataque é compartilhado com outra nota |
| intervalo_melodico_medio | média de abs(delta altura) entre ataques consecutivos, usando a nota mais aguda de cada ataque |
| pc0..pc11 | histograma de classes de altura (altura % 12, 0 = dó, não transposto), ponderado pela duração, soma 1 |
| entropia_pc | entropia de Shannon (bits) do histograma pc; máx. log2(12) = 3,58 |
