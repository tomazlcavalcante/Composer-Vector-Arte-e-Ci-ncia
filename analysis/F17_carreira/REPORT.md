# F17 - Mudança de estilo dentro da carreira (H21)

## Hipótese (registrada no DIARIO antes de rodar, ciclo 5)

**H21 (mudança de estilo dentro da carreira, idioma de Meyer):** nos compositores com opus em ordem aproximadamente cronológica (Scriabin, Beethoven, Brahms, Schumann, Rachmaninoff, Prokofiev, Fauré, Grieg, Medtner), a posição da peça no eixo do tempo do mapa (PC1) correlaciona positivamente com o número de opus. Previsão mais forte: Scriabin. Exclusões: opus póstumos de Chopin (> 65) e de Mendelssohn (> 72), que não seguem a cronologia. Teste: Spearman por compositor e meta-análise simples (sinal dos ρ e média ponderada por n). Nulo: permutar os opus dentro do compositor.

## Método

- Base: camada 6, mean, CV_WINDOWS=1,2, sem duplicatas (2.103 peças). PCA dos centróides com PC1 orientado pelo nascimento, como em `D1_explorador/export.py`; peças projetadas com `Pp = (Z - Cm) @ Vt[:2].T`. O PC1 explica 33,8% da variância.
- Opus extraído do título por regex `\bOp(?:\.|us)\s*(\d+)`. WoO, Anh., BWV, K., Hob., EG etc. ficam sem opus; "Op.posth" é excluído. Chopin só com opus <= 65; Mendelssohn só com opus <= 72. Mínimo de 8 peças com opus por compositor (todos passaram).
- Spearman entre opus e PC1; p bilateral por 5.000 permutações dos opus dentro do compositor (também p unilateral, pois H21 prevê ρ > 0).
- Opcional: Spearman entre opus e a distância cosseno ao centróide do período seguinte (Beethoven: românticos; Scriabin: modernos; demais: o próprio período), sem o compositor no centróide.
- Meta: número de ρ > 0 (teste de sinal unilateral), média dos ρ ponderada por raiz de n, com p por permutação conjunta.

## Resultados

| Compositor | n | ρ (opus × PC1) | p (bilateral) | p (unilateral) | ρ (opus × dist.) | p |
|---|---|---|---|---|---|---|
| Scriabin | 54 | 0,055 | 0,693 | 0,343 | -0,119 | 0,390 |
| Beethoven | 39 | 0,055 | 0,734 | 0,376 | -0,125 | 0,447 |
| Brahms | 18 | 0,136 | 0,601 | 0,296 | -0,313 | 0,208 |
| Schumann | 30 | 0,261 | 0,163 | 0,077 | -0,270 | 0,147 |
| Rachmaninoff | 13 | -0,154 | 0,620 | 0,696 | 0,000 | 1,000 |
| Prokofiev | 26 | -0,069 | 0,742 | 0,637 | 0,052 | 0,810 |
| Fauré | 30 | -0,281 | 0,135 | 0,932 | 0,269 | 0,137 |
| Grieg | 21 | 0,382 | 0,091 | 0,042 | -0,197 | 0,387 |
| Medtner | 32 | -0,298 | 0,100 | 0,950 | 0,136 | 0,458 |
| Chopin (op. <= 65) | 50 | 0,441 | 0,002 | 0,001 | -0,391 | 0,006 |
| Mendelssohn (op. <= 72) | 10 | 0,345 | 0,338 | 0,169 | -0,261 | 0,468 |

Combinação:

- Nove compositores da H21: 5 com ρ > 0, sinal p = 0,50; média ponderada por raiz de n = 0,008.
- Com Chopin e Mendelssohn (11): 7 com ρ > 0, sinal p = 0,27; média ponderada = 0,079, p de permutação unilateral = 0,092.

## Veredito

**H21 não confirmada.** A previsão mais forte falhou: Scriabin tem ρ = 0,05 (p = 0,69), assim como Beethoven. Entre os nove compositores previstos, o sinal é de moeda (5 de 9) e a média é praticamente zero. O único caso claro é Chopin (ρ = 0,44, p = 0,002), que entrou como caso com exclusão e não como alvo; os outros dois com sinal marginal, Grieg e Schumann, não passam com correção para 11 testes. A distância ao período seguinte não muda o quadro (só Chopin, com sinal esperado). Leitura: o PC1 mede principalmente o estilo/gênero da peça, e dentro de uma carreira ele não segue o opus de forma detectável, com poder baixo para efeitos pequenos.

## Ressalvas

- O opus é um proxy imperfeito de data: publicação não é composição (Beethoven, Brahms, Schumann e Medtner têm opus publicados fora de ordem; opus póstumos e obras reunidas distorcem). Isso atenua qualquer ρ.
- Poucas peças por compositor (10 a 54), então só efeitos moderados ou grandes seriam detectados. Ausência de significância não é ausência de efeito.
- Opus repetidos (peças do mesmo opus) geram empates; a permutação os trata corretamente, mas reduz a informação.
- O PC1 explica cerca de 34% da variância: é um eixo grosso, e a mudança de estilo de uma carreira pode estar em outras direções.
- Peças de gêneros diferentes dentro do mesmo compositor (estudos, sonatas, variações) misturam gênero com época.
- A distância ao período seguinte é exploratória; para compositores cujo "próximo período" é o próprio, o sinal esperado não é bem definido.

## Arquivos

`run.py`, `metrics.json`, `resultados_compositores.csv`, `pecas_opus.csv`, `figs/carreira.png`.
