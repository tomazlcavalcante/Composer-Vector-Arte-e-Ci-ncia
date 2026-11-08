# F13 / C3: o fio brasileiro (H14)

Base sem duplicatas (08/11): números atualizados; conclusões inalteradas. A parte descritiva (tabela "Descritivo" e o ranking de centróides, vindos do `metrics.json`) não foi refeita e segue na base anterior; as valsas (`valsas_metrics.json`) foram refeitas.

Camada 6, pooling mean, 2 janelas (1 e 2), espaço centrado e normalizado como na F3. Centróide do ragtime = média das 83 peças de Joplin, Scott; Scott, James; e Johnson, Charles Leslie (não inclui Cyril Scott). Para peças de ragtime e de Chopin, o próprio centróide é calculado sem a peça. Tico-Tico (Abreu, include_extra): 1 peça.

## H14: confirmada, exploratória (valsas ficam longe do ragtime e perto de Chopin)
H14 (tangos/maxixes de Nazareth mais perto do ragtime que as valsas) não era testável pela regex de títulos (1 tango, 0 valsa; ver `nazareth_classes.csv`). Os gêneros de 13 das 22 peças foram então verificados em fontes externas pelo coordenador (`nazareth_generos_verificados.csv`):

- **Valsas (4)**
  - Confidências: IMSLP ("Alternative Title: Valsa", 1913); choromusic.com (waltz).
  - Coração que sente: partitura da Musica Brasilis ("Valsa", 1903).
  - Resignação: texto do site Ernesto Nazareth 150 anos ("a valsa Resignação", 1930).
  - Rosa Maria: loja de partituras Musicroom ("slow valsa"); é a fonte mais fraca, comercial.
- **Polcas e tangos brasileiros (8)**
  - Polcas: Apanhei-te, cavaquinho; Ameno Resedá.
  - Tangos brasileiros: Brejeiro, Bambino, Odeon, Fon-Fon (es-academic e outras fontes); Escovado (choromusic); Tango Habanera (só pelo título).
- **Fado (1):** Ferramenta, fora dos dois grupos.
- **Não verificados (9):** os demais títulos (inclui 1922, A bela Melusina etc.).

**Resultados** (eixo único, recalculado em `valsas.py`: centróide do ragtime = 79 rags, sem as 4 valsas de ragtime; rags sem a própria peça; Chopin como antes):

| Grupo | n | Dist. ao ragtime | Dist. a Chopin |
|---|---|---|---|
| Nazareth, valsas | 4 | 1,096 | 0,417 |
| Nazareth, tangos e polcas | 8 | 0,546 | 1,085 |
| Ragtime, peças "waltz" no título | 4 | 0,452 | 0,824 |
| Ragtime, demais rags | 79 | 0,216 | 1,208 |

- Nazareth, 4 valsas contra 8 tangos e polcas: Mann-Whitney unilateral p = 0,002 tanto para distância ao ragtime (valsas maiores) quanto a Chopin (valsas menores). Separação completa (U = 32 de 32), o menor p possível com 4 contra 8. Sem Rosa Maria (3 contra 8), p = 0,006 nos dois casos, o mínimo possível nesse desenho.
- Ragtime, valsas contra rags: as 4 peças com "waltz" no título (Joplin: Augustan Club, Binks', Harmony Club; C. L. Johnson: Wedding of the Fairies) ficam mais perto de Chopin que os 79 rags (0,824 contra 1,208; p = 0,0003) e mais longe do centróide do ragtime (0,452 contra 0,216; p = 0,0005).
- Tico-Tico (centróide sem valsas): 0,437 ao ragtime, 1,410 a Chopin.
- Nota de método: o primeiro cálculo (feito antes de `valsas.py`) usava o centróide com as valsas para Nazareth (valsas 1,086; tangos e polcas 0,540; valores dessa versão, anteriores à remoção das cópias) e sem elas para o teste de ragtime. `valsas.py` refaz tudo com o centróide sem valsas, e os p não mudam. Valores por peça em `valsas_distancias.csv`; resumo em `valsas_metrics.json`.

Figura: `figs/valsas.png` (distância ao ragtime x distância a Chopin, por peça, com as valsas de Nazareth e de ragtime rotuladas).

**Ressalvas**
- n muito pequeno (4 valsas, 8 tangos e polcas, 4 valsas de ragtime), análise exploratória; o p = 0,002 é o piso do desenho, não evidência forte.
- Valsa e tango diferem em compasso (3/4 contra 2/4). O modelo pode estar captando o compasso diretamente. Isso é exatamente o tipo de propriedade estrutural de gênero que se esperaria que ele capte, e não prova que ele "reconhece" a valsa como categoria estilística, nem que as outras causas (andamento lento, textura romântica, transcrição MIDI) estejam descartadas.
- Rosa Maria vem de fonte comercial (Musicroom); sem ela o resultado se mantém no mínimo possível (p = 0,006).
- Os demais 9 títulos de Nazareth (mais Ferramenta, fado) não foram verificados; o rótulo de Tango Habanera vem só do título. Valsas de ragtime foram identificadas pela palavra "waltz" no título.

## Descritivo

*Base anterior (2.183 peças): vem do `metrics.json`, que não foi refeito. Os valores devem mudar pouco (o ragtime e Nazareth mantêm o mesmo número de peças), mas não foram recalculados.*
| Grupo | n | Dist. ao ragtime | Dist. a Chopin |
|---|---|---|---|
| Ragtime (ref.) | 83 | 0,228 | 1,196 |
| Nazareth | 22 | 0,628 | 0,934 |
| Villa-Lobos | 22 | 1,171 | 0,899 |
| Tico-Tico | 1 | 0,441 | 1,409 |

- Nazareth, no conjunto, é o compositor (entre 49 fora do grupo ragtime) mais próximo do centróide do ragtime (0,354 entre centróides; 2º é Czerny, 0,579). 18 das 22 peças ficam mais perto do ragtime que de Chopin. Esta é uma observação sobre o compositor inteiro, não sobre os tangos.
- A distribuição de Nazareth é bimodal: a maioria das peças fica perto do ragtime (0,24 a 0,66), mas Confidências, Coração que sente, Resignação e Rosa Maria ficam longe do ragtime (0,94 a 1,30) e perto de Chopin (0,39 a 0,45); Elétrica e Ferramenta estão no meio. Essas quatro são as valsas verificadas (ver H14 acima).
- Villa-Lobos cai longe do ragtime (média 1,17; 47º de 49 por centróide) e a meio caminho de Chopin; apenas 9 das 22 peças estão mais perto do ragtime que de Chopin. Não há sinal de fio ragtime nele neste espaço.
- Tico-Tico (1 peça) fica perto do ragtime (0,44) e longe de Chopin (1,41), na região de Nazareth (distância ao centróide de Nazareth 0,49). Um único caso, ilustrativo.

## Contexto e cautelas
Em termos gerais, é conhecido que choro, maxixe e tango brasileiro e o ragtime compartilham raízes na habanera e na polca sincopada, o que torna plausível a proximidade de Nazareth, mas este resultado não prova a ligação: a proximidade pode refletir apenas andamento, textura de acompanhamento em colcheias, tessitura ou tipo de transcrição MIDI. O espaço de Nazareth também é contaminado por peças lentas ao estilo romântico. A amostra é pequena (22 peças; 1 peça de Tico-Tico) e a análise é exploratória.

Arquivos: `metrics.json`, `pecas.csv`, `nazareth_classes.csv`, `nazareth_generos_verificados.csv`, `ragtime_valsas.csv`, `valsas.py`, `valsas_distancias.csv`, `valsas_metrics.json`, `figs/brasil.png`, `figs/valsas.png`.
