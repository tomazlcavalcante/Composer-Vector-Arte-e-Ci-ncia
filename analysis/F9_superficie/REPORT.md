# F9 — O modelo sabe mais que estatística de superfície? (bloco A)

Base sem duplicatas (08/11): números atualizados; conclusões inalteradas.

## Pergunta
A organização cronológica dos compositores no espaço do modelo se reduz a estatísticas simples de superfície (densidade de notas, registro, duração, polifonia, intervalos, classes de altura)?

## Hipóteses registradas (PLANO_V2, antes dos resultados)
- **H8:** o mapa só de descritores também correlaciona com a época, mas menos que o do modelo (Mantel menor).
- **H9:** a RSA entre o mapa do modelo e o dos descritores é moderada, abaixo de 0,7; o modelo não se reduz aos descritores.
- **H10:** a cronologia sobrevive à remoção dos descritores, com ρ > 0,3.
- **H11:** a correlação surpresa × época cai ao controlar os descritores, mas não some.

## Configuração
- Camada 6, pooling média, 2 janelas por peça (1 e 2); 2.103 peças, 52 compositores.
- 24 descritores simbólicos por janela, calculados só dos eventos MIDI e sem o modelo (ver `DESCRITORES.md`), médios por peça e padronizados.
- A2: centróides por compositor no espaço dos descritores; Mantel (Spearman, 5.000 permutações) contra |Δ nascimento|; RSA com a matriz de distâncias do modelo.
- A3: regressão linear dos descritores para fora das representações das peças; com os resíduos, refaz Mantel, R² do compositor e acurácia da sonda (regressão logística, 5 dobras, acurácia balanceada).
- A4: surpresa × época com controle linear dos descritores (nível de compositor e de peça).
- Script: `run.py`; números em `metrics.json`.

## Resultado
| | Mantel ρ | R² do compositor | Sonda |
|---|---|---|---|
| Modelo (base, H1) | 0,502 (p = 0,0002) | 0,268 | 0,311 |
| Só descritores (H8) | 0,207 (p = 0,0002) | 0,182 | 0,223 |
| Modelo sem descritores (H10) | 0,356 (p = 0,0002) | 0,152 | 0,280 |

- **Quanto o modelo é descritores:** os descritores explicam cerca de 50% da variância das representações do modelo (0,504).
- **H8:** o mapa só de descritores acompanha a época (0,207), bem menos que o do modelo (0,502). Confirmada.
- **H9:** RSA modelo × descritores = 0,650, abaixo de 0,7. Confirmada, mas 0,65 não é pequena: os dois mapas compartilham muito.
- **H10:** removidos os descritores, a cronologia continua (0,356 > 0,3; queda de 0,502) e a sonda cai pouco (0,311 → 0,280). O R² do compositor cai mais, de 0,268 para 0,152. Confirmada.
- **H11 (surpresa):** os descritores explicam 72% da surpresa (R² = 0,72). Mesmo assim a relação com a época sobrevive no nível do compositor: 0,499 → 0,404 (p = 0,003). No nível da peça, 0,329 → 0,210. Confirmada: cai, mas não some.
- Figura-síntese: `figs/controles_cronologia.png`, com os controles de superfície (esta análise) e de gênero (F10: 0,374).

## Comparação com o nulo
- Mantel: p vem de permutar os compositores; 0,0002 = 1/5001 é o mínimo possível, então os três ρ estão acima do nulo, sem que o p distinga entre eles.
- Nulo da figura: 1.000 permutações dos nascimentos entre os centróides do modelo dão p95 ≈ 0,104 (máximo 0,228; valores calculados em tempo de execução pela `fig_controles.py`, não guardados no `metrics.json`; o da base anterior). Todas as linhas ficam acima dele, inclusive a só de descritores (0,207), embora esse nulo tenha sido calculado no espaço do modelo e valha só como referência de ordem de grandeza para ela.
- Não há nulo próprio para a diferença entre 0,502 e 0,356, nem IC; a queda não foi testada.
- H11: p = 0,003 só para o nível do compositor controlado; sem p para o nível da peça.

## O que NÃO se pode concluir
- Não se conclui que a cronologia é independente da superfície: os descritores levam cerca de 29% do ρ (0,502 → 0,356) e 72% da surpresa.
- Os descritores são simples e lineares, e a regressão linear não remove relações não lineares com as representações. Superfície mais rica ou não linear poderia reduzir mais o ρ restante.
- As classes de altura não estão transpostas (0 = dó), o que inclui a tonalidade. O controle trata a tonalidade como descritor de superfície, e o modelo pode carregar tonalidade por outros caminhos.
- A base tem 2 janelas por peça (trechos curtos); os descritores valem para esses trechos, não para a peça inteira.
- O ρ restante não prova que o modelo "conhece" a história: pode ser gênero, instrumentação, gravação ou transcrição (ver F10 e `F6_controles/VALIDADE.md`).
- A sonda cair pouco não diz que a identidade do compositor independe da superfície: o R² do compositor cai de 0,268 para 0,152.
- Mantel com 52 compositores e metadados de nascimento não verificados em fonte externa.

## Figuras
- `figs/controles_cronologia.png`: "A cronologia sobrevive aos controles" (barras do Mantel ρ por controle, com o p95 aproximado do nulo). Script: `fig_controles.py`.
