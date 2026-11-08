# F14: compasso ou gênero? (H15)

## Pergunta
O agrupamento das valsas (F13: valsas de Nazareth e de ragtime ficam perto de Chopin e longe de tangos e rags) é específico da valsa ou vale para qualquer dança em compasso ternário? A ressalva da F13 era justamente que o modelo poderia estar captando só o 3/4.

## Hipótese registrada (H15, escrita antes dos resultados)
"Se o agrupamento for só compasso, as outras danças ternárias (minuetos, mazurcas, polonaises) devem ficar tão perto das valsas quanto as valsas ficam entre si, e mais perto delas do que das binárias, dentro do mesmo compositor."
**Refutação:** as valsas se agrupam entre si, mas as outras ternárias não ficam mais perto das valsas do que das binárias.

## Configuração
Camada 6, pooling mean, janelas 1 e 2, nível de peça, espaço centrado e normalizado (L2), distância cosseno. Classes por regex no título (case-insensitive), nesta ordem de prioridade:
- **valsa:** `valse|valsa|waltz|walzer`
- **outras ternárias:** `menuet|minuet|minueto|mazur|polonaise|polacca|sarabande|ländler|landler`
- **binárias:** `polka|polca|march|marche|marcha|galop|rag\b|tango|maxixe|schottisch|gavotte|bourr|two-step|cake ?walk`

Nenhum título casou com mais de uma regex. Contagem bruta: 88 valsas, 121 ternárias, 86 binárias (295 de 2183 peças). Por compositor e classe: `contagens.csv`.

**Dois filtros adicionados por mim (não estavam no pedido), porque o regex sozinho contamina a análise:**
1. **MIDIs duplicados.** 117 peças (37 grupos, sempre dentro de um mesmo compositor) têm vetor e perda idênticos com títulos diferentes (ex.: Godard, Valse No. 2, 3, 6, 7, 10, 15 são o mesmo vetor; 12 peças de Handel, "Air in F major, HWV 591" e 11 minuetos, idem). Isso gera distâncias 0 e infla a "proximidade" dentro do compositor. Cada grupo conta como uma peça só se todos os títulos têm a mesma classe; grupos de classe mista ou sem classe saem (28 peças classificadas pelo regex estavam em grupos duplicados). Após isso: 78 valsas, 105 ternárias, 84 binárias.
2. **"Variations".** Títulos com "variation" (ex.: "Variations on a March", "Variations on a Minuet") não são danças e saem (5 peças).
A análise com o regex literal, sem os dois filtros, está em `metrics.json` (`regex_literal_sem_dedup`) e dá a mesma conclusão.

## Resultado

### 2. Dentro do compositor (peças do mesmo compositor; média por compositor)
Compositores com as três classes (n = 10): Balakirev, Beethoven, Chaminade, Chopin, Godard, Lack, Liszt, Raff, Scharwenka, Schubert. Teste de Wilcoxon pareado por compositor. IC 95% = bootstrap sobre compositores.

| Comparação | n | média A | média B | dif. (A − B) [IC 95%] | A menor em | p bilateral |
|---|---|---|---|---|---|---|
| (a) valsa–ternária vs valsa–binária (é o compasso?) | 10 | 0,747 | 0,756 | −0,008 [−0,080; 0,082] | 7/10 | 0,43 |
| (b) ternária–binária vs valsa–binária | 10 | 0,642 | 0,756 | −0,113 [−0,272; 0,050] | 7/10 | 0,16 |
| (c) valsa–valsa vs valsa–ternária | 10 | 0,660 | 0,747 | −0,088 [−0,141; −0,039] | 9/10 | 0,004 |
| (d) valsa–valsa vs valsa–binária | 10 | 0,660 | 0,756 | −0,096 [−0,170; −0,020] | 7/10 | 0,049 |
| (e) ternária–ternária vs ternária–binária | 8 | 0,647 | 0,600 | +0,047 [−0,085; 0,204] | 4/8 | 0,95 |

Leitura:
- (a) A distância de uma valsa a uma ternária do mesmo compositor é indistinguível da distância a uma binária (diferença de 0,008, mediana −0,056, 7 de 10 compositores a favor). Pelo critério de H15, o compasso deveria deixar V–T claramente menor que V–B.
- (c) As valsas ficam mais perto umas das outras do que de outras ternárias (9 de 10 compositores).
- (b) T–B é menor que V–B, mas o IC cobre zero (p = 0,16). O que se vê é que a valsa é a classe afastada: ela está longe tanto de ternárias quanto de binárias, e ternárias e binárias não se separam bem entre si (e: p = 0,95).
- Robustez: sem Chopin (n = 9), (a) +0,004 (p = 0,65), (c) −0,093 (n = 11, p = 0,002). Com o regex literal e sem dedup, (a) +0,009 (n = 10, p = 0,70), (c) −0,104 (n = 12, p = 0,0015).
- **Contraexemplo parcial.** Se "outras ternárias" forem só minueto, Ländler e sarabande (sem mazurcas e polonaises, que são danças de salão polonesas e dominadas por Chopin), restam 5 compositores: V–T 0,840 contra V–B 0,916 (−0,076 [−0,114; −0,038]), a favor em 5 de 5, p bilateral = 0,0625 (o mínimo possível com n = 5). Isto é compatível com algum efeito de compasso para essas danças, mas o n é minúsculo e o teste não passa a 5% bilateral. V–V contra V–T nesse subconjunto: −0,103, 5 de 6, p = 0,0625.

### 3. Entre compositores
**Lógica.** Os dois centróides de referência são ambos de Chopin: valsas (9) e mazurcas (23, regex `mazur`, inclui "Allegretto and Mazurka" e "Rondo à la mazur"). Como os dois vêm do mesmo compositor, a identidade de Chopin se cancela na diferença `d(valsas de Chopin) − d(mazurcas de Chopin)`: negativo = mais perto das valsas, positivo = mais perto das mazurcas. Mazurcas são ternárias, mas de outro caráter (acento no tempo 2 ou 3, mais rústico). Se o agrupamento fosse só compasso, tudo que é ternário deveria ficar do lado negativo ou neutro. Para peças de Chopin o centróide é refeito sem a própria peça. Os números abaixo são de peças de outros compositores (Chopin fica de fora).

| Classe (outros compositores) | peças / compositores | d às valsas de Chopin | d às mazurcas de Chopin | dif. por peça | peças mais perto da valsa | compositores mais perto da valsa (dif. média por compositor) | p Wilcoxon (compositores) |
|---|---|---|---|---|---|---|---|
| valsa | 69 / 22 | 0,774 | 0,817 | −0,043 | 57% | 14/22 (−0,051) | 0,042 |
| mazurca | 21 / 11 | 0,781 | 0,698 | +0,083 | 19% | 3/11 (+0,050) | 0,28 |
| minueto | 29 / 12 | 1,022 | 1,036 | −0,014 | 59% | 4/12 (+0,078) | 0,20 |
| outra ternária (polonaise, Ländler, sarabande) | 21 / 9 | 0,907 | 0,833 | +0,074 | 38% | 3/9 (+0,093) | 0,098 |
| binária | 82 / 23 | 0,952 | 0,952 | +0,001 | 52% | 10/23 (+0,019) | 0,46 |

Verificação: dentro de Chopin (sem a própria peça), as mazurcas ficam mais perto das mazurcas (dif +0,223; 96% das peças) e as valsas mais perto das valsas (−0,045; 67%), como deveria.

Leitura:
- **Valsas de outros compositores** ficam mais perto das valsas de Chopin que das mazurcas, mas o efeito é pequeno e ruidoso (−0,043 por peça; 14 de 22 compositores; p = 0,04 sem correção para os vários testes desta tabela).
- **Mazurcas de outros compositores** vão no sentido oposto (81% das peças mais perto das mazurcas de Chopin), embora por compositor o n seja só 11 e o p não passe de 0,28. Isso sugere que há um eixo valsa e outro mazurca, e não um bloco ternário único.
- **Minuetos e outras ternárias** não ficam mais perto das valsas: por compositor, 4/12 e 3/9 do lado da valsa. A distância absoluta de minuetos às valsas de Chopin (1,02) é maior que a das valsas de outros compositores (0,77) e parecida com a das binárias (0,95).
- A linha "binária" é a referência de nível: não tem preferência (dif ≈ 0).

**Minuetos clássicos (Mozart, Bach, Beethoven; Handel como extra; Haydn não aparece nas classes).** Para cada compositor de minuetos, distância média de cada minueto às peças de outros compositores, em quatro grupos (época × compasso). "Cedo" = nascidos até 1800; "tarde" = depois. O compositor do minueto é excluído dos grupos. Isso separa compasso de época: se os minuetos estivessem perto de "qualquer valsa" por serem ternários, estariam perto das valsas tardias também.

| Compositor (n minuetos) | valsa cedo | binária cedo | valsa tarde | binária tarde |
|---|---|---|---|---|
| Mozart (7) | 0,932 | 0,994 | 1,181 | 0,983 |
| Bach (4) | 0,953 | 1,158 | 1,202 | 1,028 |
| Beethoven (1) | 0,823 | 0,898 | 1,029 | 0,930 |
| Handel (7, extra) | 0,949 | 1,036 | 1,155 | 1,021 |

Tamanhos dos grupos: valsa cedo 8 a 11 peças (só Beethoven e Schubert; Schubert domina), binária cedo 12 a 13 (5 compositores), valsa tarde 67 (21 compositores), binária tarde 71 (19 compositores).
- Contra as **valsas tardias**, os minuetos ficam mais longe do que das binárias tardias (por 0,10 a 0,20), nos quatro compositores.
- Contra as **valsas cedo** (basicamente Schubert e Beethoven), os minuetos ficam um pouco mais perto do que das binárias cedo (0,06 a 0,20), mas o grupo é quase um compositor só. Quase tudo que o 3/4 "explica" aqui é a vizinhança de Schubert/Beethoven, não "valsa de qualquer compositor".
- Resposta para a pergunta: minuetos não ficam mais perto das valsas de qualquer compositor. A proximidade existe só para valsas da própria época (e quase só de Schubert); para as valsas românticas é o contrário. As binárias da época não ganham da valsa cedo, mas também não há grupo binário de época tão homogêneo (a binária tardia inclui ragtime, que é distante de tudo).

## Veredito de H15
**H15 refutada, com cautela.** Segundo o critério de refutação registrado: (i) as valsas se agrupam entre si (V–V < V–T em 9 de 10 compositores, p = 0,004) e (ii) as outras ternárias não ficam mais perto das valsas do que as binárias (V–T ≈ V–B: −0,008; p = 0,43). Entre compositores, minuetos e polonaises não se aproximam das valsas de Chopin. O sinal contrário, mais fraco, vem de minuetos, Ländler e sarabandes dentro do compositor (5 de 5 a favor, p = 0,0625), que pede mais dados antes de se descartar um efeito parcial de compasso.

## Comparação com o nulo
Os testes pareados por compositor são exatos (Wilcoxon), sem nulo de permutação de rótulos. Com n = 5 o menor p bilateral possível é 0,0625; com n = 10, 0,002. Os p não têm correção para múltiplos testes (5 comparações na parte 2, 5 classes na parte 3).

## O que não se pode concluir
- Que o modelo "conhece" a valsa como categoria. O agrupamento pode vir de andamento, textura de acompanhamento (baixo no tempo 1, acordes nos 2 e 3), região de teclado ou época. Danças binárias e ternárias comparadas aqui também diferem em outras coisas além do compasso.
- Que o compasso não importa. A diferença valsa contra ternária é grande onde há n; o efeito de compasso pode existir e ser pequeno demais para este n.
- Que a ressalva da F13 está resolvida: ela perde força (valsa é distinta de outras ternárias), mas "outras ternárias" aqui são sobretudo mazurcas e polonaises de Chopin, Balakirev e Scriabin, de caráter muito diferente de minuetos.
- Títulos são rótulos imperfeitos: "Valse" pode ser uma valsa lenta, uma "valse-impromptu" ou uma peça de caráter; uma "Polonaise" pode estar em compasso binário composto; "Mazurka" em 3/4 ou 3/8; "March" pode ter um trio ternário; "Ländler" é tipicamente ternário rápido. Não verifiquei o compasso real das peças.
- n por compositor é pequeno (1 a 9 peças por classe; 10 compositores nas três classes; 5 no subconjunto estrito). Alguns compositores têm distâncias internas muito baixas por razões de repertório (Scharwenka, Lack), e cada um pesa igual na média.
- Duplicatas de MIDI com títulos diferentes (ver Configuração) sugerem erro de metadados no corpus; os filtros aplicados são conservadores, mas outras duplicatas parciais (vetores quase idênticos, d < 0,03) podem existir.

## Figuras
`figs/compasso.png`: painel A, distâncias médias por compositor (valsa–valsa, valsa–ternária, ternária–binária, valsa–binária); painel B, diferença de distância às valsas e às mazurcas de Chopin por classe, para peças de outros compositores.

## Ideias fora do escopo
- Anotar o compasso real por peça (a partir dos MIDIs) em vez de usar título, e repetir a análise com compasso como variável contínua.
- Auditar duplicatas de MIDI (vetor e perda idênticos) nas outras frentes (F3, F4, F13): elas afetam distâncias dentro do compositor, dispersão e contagens por compositor.
- Replicar com valsas lentas e rápidas separadas, e com Haydn (hoje sem peça classificada).

## Arquivos
`run.py`, `metrics.json`, `contagens.csv`, `dentro_compositor.csv`, `entre_compositores.csv`, `minuetos_classicos.csv`, `figs/compasso.png`.
