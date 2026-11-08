# F13 / C3: o fio brasileiro (H14)

Camada 6, pooling mean, 2 janelas (1 e 2), espaço centrado e normalizado como na F3. Centróide do ragtime = média das 83 peças de Joplin, Scott; Scott, James; e Johnson, Charles Leslie (não inclui Cyril Scott). Para peças de ragtime e de Chopin, o próprio centróide é calculado sem a peça. Tico-Tico (Abreu, include_extra): 1 peça.

## H14 não pôde ser testada
Classificação por título (regex): das 22 peças de Nazareth, **1** cai em tango/maxixe/choro ("Tango Habanera"), **0** em valsa e 21 em "outro". Com n = 1 contra 0 o Mann-Whitney é impossível. A lista de títulos e classes está em `nazareth_classes.csv`. Títulos de Nazareth costumam nomear a peça sem o gênero, então seria preciso uma rotulagem externa (partituras ou catálogo), que não foi feita aqui. Não foi inventado nenhum rótulo.

## Descritivo
| Grupo | n | Dist. ao ragtime | Dist. a Chopin |
|---|---|---|---|
| Ragtime (ref.) | 83 | 0,228 | 1,196 |
| Nazareth | 22 | 0,628 | 0,934 |
| Villa-Lobos | 22 | 1,171 | 0,899 |
| Tico-Tico | 1 | 0,441 | 1,409 |

- Nazareth, no conjunto, é o compositor (entre 49 fora do grupo ragtime) mais próximo do centróide do ragtime (0,354 entre centróides; 2º é Czerny, 0,579). 18 das 22 peças ficam mais perto do ragtime que de Chopin. Esta é uma observação sobre o compositor inteiro, não sobre os tangos.
- A distribuição de Nazareth é bimodal: a maioria das peças fica perto do ragtime (0,24 a 0,66), mas Confidências, Coração que sente, Resignação e Rosa Maria ficam longe do ragtime (0,92 a 1,29) e perto de Chopin (0,40 a 0,46); Elétrica e Ferramenta estão no meio. Os títulos sozinhos não permitem dizer se essas quatro são valsas ou peças lentas; vale conferir à mão como hipótese para uma rotulagem posterior.
- Villa-Lobos cai longe do ragtime (média 1,17; 47º de 49 por centróide) e a meio caminho de Chopin; apenas 9 das 22 peças estão mais perto do ragtime que de Chopin. Não há sinal de fio ragtime nele neste espaço.
- Tico-Tico (1 peça) fica perto do ragtime (0,44) e longe de Chopin (1,41), na região de Nazareth (distância ao centróide de Nazareth 0,49). Um único caso, ilustrativo.

## Contexto e cautelas
Em termos gerais, é conhecido que choro, maxixe e tango brasileiro e o ragtime compartilham raízes na habanera e na polca sincopada, o que torna plausível a proximidade de Nazareth, mas este resultado não prova a ligação: a proximidade pode refletir apenas andamento, textura de acompanhamento em colcheias, tessitura ou tipo de transcrição MIDI. O espaço de Nazareth também é contaminado por peças lentas ao estilo romântico. A amostra é pequena (22 peças; 1 peça de Tico-Tico) e a análise é exploratória.

Arquivos: `metrics.json`, `pecas.csv`, `nazareth_classes.csv`, `figs/brasil.png`.
