# F16 — Dialeto nacional dentro dos românticos (H18)

## Hipótese registrada (antes dos resultados)

**H18:** dentro dos compositores com `periodo == "Romântico"` (`incluir == 1`), o Mantel parcial da mesma nacionalidade, controlando |Δ nascimento|, tem ρ > 0 (mesma nacionalidade aproxima os centróides). Motivo: o H2 global teve pouca potência.

## Método

Camada 6, mean, janelas 1 e 2, sem duplicatas; peças centradas e normalizadas na base inteira e centróides só dos românticos (como em F3): 33 compositores, 1.217 peças, 528 pares, dos quais 72 de mesma nacionalidade. Distância cosseno entre centróides. Resíduo da distância numa regressão linear em |Δ nascimento|; Spearman entre o (negativo do) resíduo e a indicadora de mesma nacionalidade. p unicaudal (ρ > 0) por 5.000 permutações dos rótulos de nacionalidade entre os compositores.

## Resultados

- ρ parcial = **−0,007**, p unicaudal = **0,52**. Nulo: média 0,000, percentil 95 = 0,094. Sem controle da época, ρ = 0,013.
- Distância vs. |Δ nascimento| dentro dos românticos: ρ = 0,16 (a época explica pouco aqui, pela faixa curta de nascimentos).

| Nacionalidade (≥ 3 românticos) | n | dist. interna | dist. aos outros românticos | diferença (fora − dentro) |
|---|---|---|---|---|
| Francês | 9 | 0,777 | 0,772 | −0,005 |
| Alemão | 8 | 0,782 | 0,776 | −0,007 |
| Russo | 3 | 0,798 | 0,781 | −0,016 |

Nenhum grupo é mais coeso que a média: a distância interna é igual ou ligeiramente maior que a externa. Pares de mesma nacionalidade não são, em média, mais próximos.

## Veredito H18

**Não confirmada.** Não há evidência de dialeto nacional entre os românticos (ρ parcial ≈ 0, bem dentro do nulo). Ausência de evidência, não evidência de ausência: o poder é baixo.

## Cautelas

- Metadados de nacionalidade só **parcialmente verificados** (só os 9 de baixa confiança foram conferidos no IMSLP; os demais vêm de conhecimento geral). Casos limítrofes (por exemplo, Gurlitt alemão/dinamarquês) e a atribuição de "Romântico" (Debussy e Satie caem aqui por `periodo`) afetam os grupos.
- n pequeno: 33 compositores, só três nacionalidades com ≥ 3 e 8 nacionalidades representadas por 1 ou 2; os 72 pares de mesma nacionalidade vêm quase todos de França e Alemanha. Os pares não são independentes (permutação de rótulos entre compositores respeita isso, mas não corrige a baixa potência).
- Centróides de poucas peças (alguns compositores) são ruidosos; "mesma nacionalidade" mistura épocas e gêneros diferentes (miniaturas de piano, canção, orquestra).
- Resultado cobre só este modelo, camada e janelas.
