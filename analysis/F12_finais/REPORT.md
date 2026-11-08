# F12 / C2: finais de obra (H13)

Camada 6, pooling mean, janelas w2 (início, 1/6), w1 (meio) e w3 (final, 5/6). Espaço centrado pela média de todas as janelas e normalizado. 2.183 peças com as 3 janelas. Centróides do compositor e do período calculados **sem a própria peça** (média das janelas das demais peças). Diferença = dist(final) − dist(início); valor negativo significa final mais perto do centróide (mais "convencional"). Perda: o npz guarda um escalar por janela, então "perda por posição" é a perda média de cada janela.

**H13: o final fica mais perto do centróide do período/compositor que o início.** Resultado: efeito minúsculo, em parte consistente, não homogêneo entre períodos. Não é evidência forte.

| Centróide | Δ médio (final − início) | Peças com final mais perto | Wilcoxon (unilateral) | Compositores com final mais perto (sinal) |
|---|---|---|---|---|
| Período | −0,0072 | 53,1% | p = 0,0012 | 33/52, p = 0,035 (bilateral 0,070) |
| Compositor | −0,0054 | 51,0% | p = 0,016 | 26/52, p = 0,56 |

Distâncias médias: ao período 0,722 (início) vs 0,714 (final); ao compositor 0,583 vs 0,577. O efeito é cerca de 1% da distância. Por período o sinal não é o mesmo:
- Romântico (n = 1272): final mais perto (Δ período −0,015, p < 1e-4; Δ compositor −0,018).
- Moderno (n = 327): final mais perto do período (−0,032, p = 1e-4; 9 de 11 compositores).
- Barroco (n = 326) e Clássico (n = 238): sentido **oposto** (Δ período +0,020 e +0,033; os finais ficam mais longe, p bilateral 0,018 e 0,013). Poucos compositores (3 e 4).
- Renascimento: 1 compositor, 20 peças, sem poder (p = 0,10; centróide do período = do compositor).
Teste por compositor: o sinal das médias é só marginal para o período e nulo para o compositor, então o resultado agregado é puxado por poucos compositores com muitas peças (Romântico).

**Pistas de banalidade (medidas):**
- Distância início ↔ final dentro da peça: 0,417, **menor** que início ↔ meio (0,435) e meio ↔ final (0,433). Início e final se parecem entre si um pouco mais do que cada um com o meio, o que pode refletir textura recorrente (abertura e coda).
- Perda média: início 2,475, meio 2,505, final 2,472. Final mais previsível que o início só por 0,003 (Wilcoxon p = 0,008; final com perda menor em 43% das peças, isto é, na maioria o final não é mais previsível). Diferença pequena demais para sustentar "finais mais previsíveis".
- Correlação (Spearman) entre Δ distância ao período e Δ perda (final − início): −0,16. Quando a perda cai no final, o final tende a ficar mais perto do centróide, o que sugere que parte do efeito é previsibilidade/textura simples, não "convenção" no sentido de Meyer.

**Cautelas:** w2 e w3 diferem em posição, e tanto introduções lentas quanto acordes finais longos mudam o embedding sem implicar convencionalidade. O centróide mistura janelas de todas as posições. Peças curtas têm janelas sobrepostas, o que aproxima início e final. Os testes por peça tratam peças do mesmo compositor como independentes (pseudo-replicação), por isso o teste por compositor é o mais conservador. Várias comparações (períodos × dois centróides) sem correção.

Arquivos: `metrics.json`, `pecas.csv`, `figs/finais.png`.
