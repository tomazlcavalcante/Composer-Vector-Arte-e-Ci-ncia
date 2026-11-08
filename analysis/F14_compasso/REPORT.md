# F14: compasso ou gênero? (H15)

Base sem duplicatas (08/11): números atualizados; conclusões inalteradas.

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

Nenhum título casou com mais de uma regex. Contagem bruta (base de 2.103 peças): 80 valsas, 108 ternárias, 85 binárias (273 de 2.103 peças). Por compositor e classe: `contagens.csv`.

**Dois filtros adicionados por mim (não estavam no pedido), porque o regex sozinho contamina a análise:**
1. **MIDIs duplicados.** Esta análise foi a que encontrou o problema: 117 peças (37 grupos, sempre dentro de um mesmo compositor) tinham vetor e perda idênticos com títulos diferentes (ex.: Godard, Valse No. 2, 3, 6, 7, 10, 15 eram o mesmo vetor; 12 peças de Handel, "Air in F major, HWV 591" e 11 minuetos, idem), o que gerava distâncias 0 e inflava a "proximidade" dentro do compositor. Desde 08/11 as 80 cópias saem na leitura comum (`analysis/data/duplicatas_remover.txt`), então o script não encontra mais grupos (`midis_duplicados.grupos = 0` no `metrics.json`). O filtro local ficou no código, sem efeito. Com a base limpa: 78 valsas, 106 ternárias, 84 binárias usadas.
2. **"Variations".** Títulos com "variation" (ex.: "Variations on a March", "Variations on a Minuet") não são danças e saem (5 peças).
A análise com o regex literal, sem o filtro de variações, está em `metrics.json` (`regex_literal_sem_dedup`; o nome é da versão anterior, e a base já está sem as cópias) e dá a mesma conclusão.

## Resultado

### 2. Dentro do compositor (peças do mesmo compositor; média por compositor)
Compositores com as três classes (n = 10): Balakirev, Beethoven, Chaminade, Chopin, Godard, Lack, Liszt, Raff, Scharwenka, Schubert. Teste de Wilcoxon pareado por compositor. IC 95% = bootstrap sobre compositores.

| Comparação | n | média A | média B | dif. (A − B) [IC 95%] | A menor em | p bilateral |
|---|---|---|---|---|---|---|
| (a) valsa–ternária vs valsa–binária (é o compasso?) | 10 | 0,745 | 0,754 | −0,009 [−0,081; 0,081] | 7/10 | 0,43 |
| (b) ternária–binária vs valsa–binária | 10 | 0,642 | 0,754 | −0,113 [−0,271; 0,049] | 7/10 | 0,16 |
| (c) valsa–valsa vs valsa–ternária | 10 | 0,657 | 0,745 | −0,088 [−0,142; −0,039] | 9/10 | 0,004 |
| (d) valsa–valsa vs valsa–binária | 10 | 0,657 | 0,754 | −0,097 [−0,171; −0,021] | 7/10 | 0,049 |
| (e) ternária–ternária vs ternária–binária | 8 | 0,646 | 0,600 | +0,047 [−0,086; 0,203] | 4/8 | 0,95 |

Leitura:
- (a) A distância de uma valsa a uma ternária do mesmo compositor é indistinguível da distância a uma binária (diferença de 0,009, mediana −0,056, 7 de 10 compositores a favor). Pelo critério de H15, o compasso deveria deixar V–T claramente menor que V–B.
- (c) As valsas ficam mais perto umas das outras do que de outras ternárias (9 de 10 compositores).
- (b) T–B é menor que V–B, mas o IC cobre zero (p = 0,16). O que se vê é que a valsa é a classe afastada: ela está longe tanto de ternárias quanto de binárias, e ternárias e binárias não se separam bem entre si (e: p = 0,95).
- Robustez: sem Chopin (n = 9), (a) +0,003 (p = 0,65), (c) −0,094 (n = 11, p = 0,002). Com o regex literal, sem o filtro de variações, (a) +0,006 (n = 10, p = 0,70), (c) −0,085 (n = 12, p = 0,001).
- **Contraexemplo parcial.** Se "outras ternárias" forem só minueto, Ländler e sarabande (sem mazurcas e polonaises, que são danças de salão polonesas e dominadas por Chopin), restam 5 compositores: V–T 0,838 contra V–B 0,915 (−0,077 [−0,115; −0,039]), a favor em 5 de 5, p bilateral = 0,0625 (o mínimo possível com n = 5). Isto é compatível com algum efeito de compasso para essas danças, mas o n é minúsculo e o teste não passa a 5% bilateral. V–V contra V–T nesse subconjunto: −0,105 (n = 6), 5 de 6, p = 0,0625.

### 3. Entre compositores
**Lógica.** Os dois centróides de referência são ambos de Chopin: valsas (9) e mazurcas (23, regex `mazur`, inclui "Allegretto and Mazurka" e "Rondo à la mazur"). Como os dois vêm do mesmo compositor, a identidade de Chopin se cancela na diferença `d(valsas de Chopin) − d(mazurcas de Chopin)`: negativo = mais perto das valsas, positivo = mais perto das mazurcas. Mazurcas são ternárias, mas de outro caráter (acento no tempo 2 ou 3, mais rústico). Se o agrupamento fosse só compasso, tudo que é ternário deveria ficar do lado negativo ou neutro. Para peças de Chopin o centróide é refeito sem a própria peça. Os números abaixo são de peças de outros compositores (Chopin fica de fora).

| Classe (outros compositores) | peças / compositores | d às valsas de Chopin | d às mazurcas de Chopin | dif. por peça | peças mais perto da valsa | compositores mais perto da valsa (dif. média por compositor) | p Wilcoxon (compositores) |
|---|---|---|---|---|---|---|---|
| valsa | 69 / 22 | 0,769 | 0,814 | −0,045 | 57% | 14/22 (−0,053) | 0,039 |
| mazurca | 22 / 12 | 0,767 | 0,690 | +0,077 | 23% | 4/12 (+0,043) | 0,30 |
| minueto | 29 / 12 | 1,017 | 1,033 | −0,016 | 59% | 4/12 (+0,076) | 0,20 |
| outra ternária (polonaise, Ländler, sarabande) | 21 / 9 | 0,903 | 0,832 | +0,072 | 38% | 3/9 (+0,090) | 0,098 |
| binária | 82 / 23 | 0,949 | 0,950 | −0,002 | 52% | 10/23 (+0,016) | 0,50 |

Verificação: dentro de Chopin (sem a própria peça), as mazurcas ficam mais perto das mazurcas (dif +0,222; 96% das peças) e as valsas mais perto das valsas (−0,046; 67%), como deveria.

Leitura:
- **Valsas de outros compositores** ficam mais perto das valsas de Chopin que das mazurcas, mas o efeito é pequeno e ruidoso (−0,045 por peça; 14 de 22 compositores; p = 0,04 sem correção para os vários testes desta tabela).
- **Mazurcas de outros compositores** vão no sentido oposto (77% das peças mais perto das mazurcas de Chopin), embora por compositor o n seja só 12 e o p não passe de 0,30. Isso sugere que há um eixo valsa e outro mazurca, e não um bloco ternário único.
- **Minuetos e outras ternárias** não ficam mais perto das valsas: por compositor, 4/12 e 3/9 do lado da valsa. A distância absoluta de minuetos às valsas de Chopin (1,02) é maior que a das valsas de outros compositores (0,77) e parecida com a das binárias (0,95).
- A linha "binária" é a referência de nível: não tem preferência (dif ≈ 0).

**Minuetos clássicos (Mozart, Bach, Beethoven; Handel como extra; Haydn não aparece nas classes).** Para cada compositor de minuetos, distância média de cada minueto às peças de outros compositores, em quatro grupos (época × compasso). "Cedo" = nascidos até 1800; "tarde" = depois. O compositor do minueto é excluído dos grupos. Isso separa compasso de época: se os minuetos estivessem perto de "qualquer valsa" por serem ternários, estariam perto das valsas tardias também.

| Compositor (n minuetos) | valsa cedo | binária cedo | valsa tarde | binária tarde |
|---|---|---|---|---|
| Mozart (7) | 0,929 | 0,993 | 1,178 | 0,981 |
| Bach (4) | 0,951 | 1,156 | 1,198 | 1,027 |
| Beethoven (1) | 0,820 | 0,897 | 1,026 | 0,929 |
| Handel (7, extra) | 0,946 | 1,035 | 1,151 | 1,019 |

Tamanhos dos grupos: valsa cedo 8 a 11 peças (só Beethoven e Schubert; Schubert domina), binária cedo 12 a 13 (5 compositores), valsa tarde 67 (21 compositores), binária tarde 71 (19 compositores).
- Contra as **valsas tardias**, os minuetos ficam mais longe do que das binárias tardias (por 0,10 a 0,20), nos quatro compositores.
- Contra as **valsas cedo** (basicamente Schubert e Beethoven), os minuetos ficam um pouco mais perto do que das binárias cedo (0,06 a 0,20), mas o grupo é quase um compositor só. Quase tudo que o 3/4 "explica" aqui é a vizinhança de Schubert/Beethoven, não "valsa de qualquer compositor".
- Resposta para a pergunta: minuetos não ficam mais perto das valsas de qualquer compositor. A proximidade existe só para valsas da própria época (e quase só de Schubert); para as valsas românticas é o contrário. As binárias da época não ganham da valsa cedo, mas também não há grupo binário de época tão homogêneo (a binária tardia inclui ragtime, que é distante de tudo).

## Veredito de H15
**H15 refutada, com cautela.** Segundo o critério de refutação registrado: (i) as valsas se agrupam entre si (V–V < V–T em 9 de 10 compositores, p = 0,004) e (ii) as outras ternárias não ficam mais perto das valsas do que as binárias (V–T ≈ V–B: −0,009; p = 0,43). Entre compositores, minuetos e polonaises não se aproximam das valsas de Chopin. O sinal contrário, mais fraco, vem de minuetos, Ländler e sarabandes dentro do compositor (5 de 5 a favor, p = 0,0625), que pede mais dados antes de se descartar um efeito parcial de compasso.

## Comparação com o nulo
Os testes pareados por compositor são exatos (Wilcoxon), sem nulo de permutação de rótulos. Com n = 5 o menor p bilateral possível é 0,0625; com n = 10, 0,002. Os p não têm correção para múltiplos testes (5 comparações na parte 2, 5 classes na parte 3).

## O que não se pode concluir
- Que o modelo "conhece" a valsa como categoria. O agrupamento pode vir de andamento, textura de acompanhamento (baixo no tempo 1, acordes nos 2 e 3), região de teclado ou época. Danças binárias e ternárias comparadas aqui também diferem em outras coisas além do compasso.
- Que o compasso não importa. A diferença valsa contra ternária é grande onde há n; o efeito de compasso pode existir e ser pequeno demais para este n.
- Que a ressalva da F13 está resolvida: ela perde força (valsa é distinta de outras ternárias), mas "outras ternárias" aqui são sobretudo mazurcas e polonaises de Chopin, Balakirev e Scriabin, de caráter muito diferente de minuetos.
- Títulos são rótulos imperfeitos: "Valse" pode ser uma valsa lenta, uma "valse-impromptu" ou uma peça de caráter; uma "Polonaise" pode estar em compasso binário composto; "Mazurka" em 3/4 ou 3/8; "March" pode ter um trio ternário; "Ländler" é tipicamente ternário rápido. Não verifiquei o compasso real das peças.
- n por compositor é pequeno (1 a 9 peças por classe; 10 compositores nas três classes; 5 no subconjunto estrito). Alguns compositores têm distâncias internas muito baixas por razões de repertório (Scharwenka, Lack), e cada um pesa igual na média.
- Duplicatas de MIDI com títulos diferentes (ver Configuração) sugeriam erro de metadados no corpus; as 80 cópias já saíram da base, mas outras duplicatas parciais (vetores quase idênticos, d < 0,03) podem existir.

## Figuras
`figs/compasso.png`: painel A, distâncias médias por compositor (valsa–valsa, valsa–ternária, ternária–binária, valsa–binária); painel B, diferença de distância às valsas e às mazurcas de Chopin por classe, para peças de outros compositores.

## Ideias fora do escopo
- Anotar o compasso real por peça (a partir dos MIDIs) em vez de usar título, e repetir a análise com compasso como variável contínua.
- Auditar duplicatas parciais (vetores quase idênticos). A auditoria de cópias exatas foi feita em 08/11 e as análises foram refeitas.
- Replicar com valsas lentas e rápidas separadas, e com Haydn (hoje sem peça classificada).

## Arquivos
`run.py`, `metrics.json`, `contagens.csv`, `dentro_compositor.csv`, `entre_compositores.csv`, `minuetos_classicos.csv`, `figs/compasso.png`.
