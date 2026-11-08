# Plano de trabalho

Versão em markdown do plano do grupo, para os subagentes lerem direto do repositório. Quando houver diferença, o documento vivo no Claude Docs é o que vale.

**Prazo: cerca de dois dias.** Seguimos a *versão de dois dias* (seção 4). O resto descreve o desenho completo.

## 1. Objetivo e escopo

Medir como o modelo organiza os compositores no espaço interno e confrontar isso com a noção de estilo de Meyer. Cada experimento responde a uma das perguntas Q1–Q4 (ver README); o que não responde a nenhuma fica de fora.

**Fora do escopo:** retreinar ou melhorar o modelo, julgar o áudio gerado, montar um classificador competitivo, fazer revisão bibliográfica extensa.

## 2. Diagnóstico (o que muda em relação ao repo original)

- **Chave de compositor:** o repo original usava só o sobrenome, o que fundia J. S. Bach (129 peças) com C. P. E. Bach e outros, Robert (33) com Clara Schumann (15), Cyril (20) com James Scott (20), W. A. (72) com Leopold Mozart (5). Aqui a chave é "Sobrenome, Nome" (`analysis/common/data.py`).
- **README antigo:** "Chopin: 309, Beethoven: 112, Bach: 67" são IDs de compositor, não contagens.
- **Vetor original:** média bruta do último token na última camada (6). O artigo escolhe a camada por sondagem. Antes de comparar vetores, é preciso subtrair a média global.
- **Agregação:** a média original é por fragmento, e as peças longas pesam mais. Aqui agregamos fragmento → peça → compositor.
- **Divisão treino/validação:** foi feita por fragmento. Qualquer sonda deve dividir por **peça**.
- **Metadados do GiantMIDI não são confiáveis:** Bach, Satie, Fauré, Brahms e Ravel aparecem como "British"; Debussy e Tchaikovsky como "unknown". Curar à mão.
- **Desbalanceamento:** 55 compositores têm ≥ 20 peças. Por nascimento: até 1700: 3; 1701–1770: 3; 1771–1830: 14; 1831–1880: 21; depois de 1880: 7; sem data: 7.
- **O que o tokenizador não vê:** não há tokens de andamento nem de pedal (`use_tempos=False`, `use_sustain_pedals=False`). A grade de tempo vem da execução transcrita.
- **Entrada do modelo:** cada fragmento tem 1024 tokens, e o modelo recebe os primeiros 1023 (`sequence[:-1]`). Os vetores originais vêm desse estado.

## 3. Princípios

1. Escolher a representação (F2) **só** com rótulos de compositor; período e nacionalidade ficam ocultos até ela estar fixada.
2. Hipóteses escritas antes dos resultados.
3. Toda proximidade vem acompanhada de um nulo (permutação de rótulos, bootstrap por peças).
4. Unidade hierárquica: fragmento → peça → compositor.
5. Medir no espaço original centrado; PCA e UMAP servem só para ilustrar, com a distorção medida.
6. Comparar com estatísticas simples (linha de base simbólica).
7. Steering: medir relendo a música gerada **sem** steering, nunca na camada onde o vetor foi somado.
8. Sementes fixas; configuração gravada em `metrics.json`; todas as frentes leem o mesmo arquivo de representações.

## 4. Versão de dois dias

| Frente | Entra | Fica para depois |
|---|---|---|
| F0 | Perda conferida num subconjunto (≈ 3,05); extração das camadas 2, 4 e 6 com dois poolings (último token, média); perda por fragmento | Demais camadas |
| F1 | Compositores com ≥ 20 peças, **sem os contemporâneos de YouTube** (decisão do grupo); metadados curados; gênero da peça por palavra-chave do título | Limiar definido por estabilidade |
| F2 | Sonda linear com divisão por peça e razão entre/intra, nas 3 camadas × 2 poolings, espaço centrado, cosseno | Branqueamento, métrica euclidiana |
| F3 | Centróides, matriz de distâncias, Mantel com ano de nascimento, PCA com distorção medida | Mantel parcial de nacionalidade, UMAP |
| F4 | Fração da variância explicada pelo compositor, dispersão com n igualado, obras atípicas | Direções de desvio, gênero contra compositor |
| F5 | Homologia de grau 0 (dendrograma) com nulo | Mapper e grau 1 |
| F6 | Tamanho amostral e transposição | Andamento, dinâmica, linha de base simbólica |
| F7 | Caminho Bach → Chopin geométrico (sem geração); piloto com 1 par, vetor centrado vs. aleatório vs. nenhum, 3 valores de α | Grade completa de steering |
| F8–F9 | Escrita pelo grupo; revisão rápida por agente independente | — |

**Cronograma**

1. **Dia 1, manhã:** copiar checkpoint, tokenizador e MIDIs para a máquina do laboratório; F0 e F1 em paralelo.
2. **Dia 1, tarde:** F2; depois F3, F4, F5 e o caminho geométrico da F7 em paralelo.
3. **Dia 1, noite:** F6 e o piloto de steering na GPU.
4. **Dia 2, manhã:** tabela de validade; o grupo escolhe as figuras.
5. **Dia 2, tarde:** interpretação à luz de Meyer e escrita.
6. **Dia 2, noite:** revisão independente e fechamento.

## 5. Hipóteses (registradas antes dos resultados)

- **H1:** a distância entre centróides cresce com a diferença de época (Mantel positivo, acima do nulo).
- **H2:** o efeito da nacionalidade é menor e pode sumir ao controlar o período.
- **H3:** o compositor explica uma minoria da variância entre peças (o estilo é mais nuvem que ponto).
- **H4:** o gênero da peça rivaliza com o compositor na organização local.
- **H5:** o espaço é um contínuo; se houver um ramo destacado, ele é o Barroco.
- **H6:** o vetor centrado desloca a música relida em direção ao alvo mais que um vetor aleatório e mais que a continuação sem steering, de forma monótona em α até a quebra.
- **H7:** no caminho Bach → Chopin a posição relida avança de forma monótona. Se os pontos intermediários caem perto dos clássicos é uma pergunta aberta.

## 6. Contrato de cada frente

- Ler de `analysis/common/` e de `$CV_EMBEDDINGS`; escrever **só** na própria pasta.
- Não alterar `common/`, não retreinar o modelo nem o tokenizador.
- Na F2, nenhum acesso a período ou nacionalidade.
- Toda afirmação numérica vem com intervalo ou nulo.
- Desvios de escopo vão para a lista "Ideias fora do escopo" do REPORT, nunca para o código.

**Modelo de `REPORT.md`:** Pergunta · Hipótese registrada · Configuração · Resultado (número + intervalo) · Comparação com o nulo · O que **não** se pode concluir · Figuras · Ideias fora do escopo.

> **Nota (08/11):** as observações sobre `use_tempos=False` e `use_sustain_pedals=False` (seção 2) valem para o tokenizador do modelo original (miditok). Os resultados finais usam o **Anticipatory Music Transformer**, cujos eventos são só (tempo em segundos, duração, nota): sem pedal (`control_change` ignorado), sem dinâmica (velocity) e sem andamento notado. Ver RESULTADOS.md.
