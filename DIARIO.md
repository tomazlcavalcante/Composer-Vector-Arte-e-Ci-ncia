# Diário de decisões

## 2026-11-07, 20:50 — mudança de cenário

- Sem acesso à máquina do laboratório. O trabalho passa a rodar no ambiente do Claude: **2 núcleos de CPU, 7 GB de RAM, sem GPU**.
- Rede do ambiente: só GitHub e PyPI. Hugging Face, Google Drive e Zenodo estão **bloqueados**. Do GiantMIDI, só há aqui os 4 MIDIs de amostra do repositório oficial.
- Proposta do Thiago: usar um modelo pré-treinado da internet e, depois, o modelo dele.

### Ordem de decisão para o modelo

1. **Modelo do Thiago**, se o `state_dict` em fp16 (~40 MB) aparecer no repositório. Tem 20M de parâmetros e roda em CPU.
2. **Modelo pré-treinado do Hugging Face**, se o domínio for liberado. Preferência: Anticipatory Music Transformer small (stanford-crfm/music-small-800k, GPT-2, ~128M parâmetros, nativo em MIDI, treinado no Lakh MIDI). Ele não viu o GiantMIDI, o que deixa a análise fora da amostra de treino.
3. **Plano C**: corpus do music21 (via pip, com rótulo de compositor e época) e descritores simbólicos, sem transformer. Responde às perguntas Q1–Q3 com um espaço de estilo explícito; a Q4 fica só geométrica.

### Dados

GiantMIDI (subconjunto com sobrenome verificado). Precisa chegar ao ambiente por GitHub (o Tomaz envia os MIDIs) ou por liberação do Google Drive.

### Orçamento de CPU

Amostra de compositores com ≥ 20 peças (sem os contemporâneos de YouTube) e até 3 janelas por peça. Comandos de até 10 minutos, com resultados salvos incrementalmente.

## 2026-11-07, 21:20 — dados e modelo no ambiente

- **Domínios liberados** (huggingface.co, Google Drive). O zip do GiantMIDI veio do notebook do Tomaz pelo app. O subconjunto `surname_checked_midis` v1.2 (7.236 MIDIs) está em `/home/claude/data/giant/surname_checked_midis`.
- **Modelo:** Anticipatory Music Transformer small (`stanford-crfm/music-small-800k`): GPT-2 com 12 camadas, d = 768, contexto de 1.024 tokens, treinado no Lakh MIDI. O código do tokenizador (`jthickstun/anticipation`) foi instalado a partir do GitHub.
- **Sanidade:** perda de 2,88 num noturno de Chopin; cerca de 2 s por janela em CPU (2 núcleos).
- **Decisão sobre a entrada:** usar o formato do treino do AMT no modo autoregressivo, `[AUTOREGRESS]` seguido de 341 eventos (tempo, duração, nota), com tempo relativo ao início da janela e no máximo 100 s. Assim o modelo vê dados no formato em que foi treinado.
- **Decisão sobre a amostra:** 51 compositores com ≥ 20 peças (5 excluídos: contemporâneos de YouTube ou identidade incerta; ver `metadata_curated.csv`), 2.184 peças. Passada 1 = janela do meio de cada peça (cerca de 75 min); passadas 2 e 3 = janelas a 1/6 e 5/6, só se houver tempo. Mais Tico-Tico (Abreu) como ilustração.
- **Decisão sobre camadas:** salvar todas as 13 (embedding + 12 blocos), com último token e média. A F2 escolhe entre elas.
- **Metadados:** curados com conhecimento geral e marcados "verificar". Corrigidos os erros do GiantMIDI (Bach, Handel, Satie, Fauré, Brahms, Poulenc estavam como "British"). Período pela regra mecânica: nascimento + 30, cortes em 1600 / 1750 / 1820 / 1900, com a coluna `fronteira`.
- **Comando para retomar:** `python3 analysis/F0_infra/extract_amt.py --pass 1 --budget-min 9`. O script é retomável e pula o que já foi feito.

## 2026-11-07, 22:40 — passada 1 concluída e primeiras análises

Base: 2.183 peças, 52 compositores, 1 janela (o meio) por peça.

- **F2 (representação):** a média sobre a janela supera o último token em todas as camadas. As camadas intermediárias são as melhores. **Escolhida: camada 6 com média.** Acurácia balanceada de 0,30 (acaso = 0,019), estabilidade dos centróides de 0,79. Secundária: camada 5. O último token, usado no artigo e no repositório original, tem no máximo 0,17. A hipótese da F2 (meio ≥ fim) se confirma; a camada 12, a última, é das piores (0,19).
- **F3 (mapa, H1/H2):** H1 confirmada. Mantel ρ = 0,48 (p < 0,001) entre a distância dos centróides e a diferença de ano de nascimento. H2: a nacionalidade tem ρ = 0,08 (p = 0,02) e some ao controlar a época (ρ = 0,04, p = 0,11). O PC1 do mapa segue a cronologia; o PC2 separa a música de dança sincopada (ragtime, Nazareth, Tico-Tico). Distorção da PCA: ρ de Spearman = 0,72.
  - Vizinhos mais próximos com sentido musical: Haydn ↔ Mozart, Bach ↔ Handel, Debussy ↔ Cyril Scott, Satie ↔ Rebikov, Medtner ↔ Schumann, Chopin → Scriabin, James Scott ↔ C. L. Johnson ↔ Joplin.
  - Tico-Tico: vizinhos C. L. Johnson, James Scott e Nazareth.
  - Ressalva: a lista de "afinidades inesperadas" por resíduo linear fica dominada por Victoria (300 anos de distância). Para o ensaio, usar a lista de vizinhos.
- **F4 (nuvens, H3/H4):** H3 confirmada. O compositor explica 23% da variância entre peças (nulo: 2,4%), e 69% das peças ficam mais perto do centróide de outro compositor: o estilo é mais nuvem que ponto. H4 **não** se confirma: o compositor pesa mais que o gênero (R² de 0,27 contra 0,13 nas mesmas peças). Mais compactos: Victoria e os ragtimes. Mais espalhados: Schubert, Schumann, Tchaikovsky, Busoni, Heller.
- **F5 (forma, H5):** não há lacuna maior que a de um nulo gaussiano sem grupos (razão 1,60, contra p95 do nulo de 2,27): o espaço é um **contínuo**. Mas a divisão em 2 grupos é estável (ARI = 0,79) e separa exatamente {Bach, Handel, Scarlatti, Haydn, Mozart, Beethoven, Hummel} de todo o resto. É um ramo "pré-romântico" (Barroco + Clássico), não só barroco.
- **F7a (caminho geométrico):** os compositores mais próximos do segmento Bach → Chopin incluem Beethoven (t = 0,39) e vários românticos com t entre 0,76 e 0,92. Dentro do segmento, t correlaciona com o ano de nascimento (ρ = 0,53).
- **F7b (steering, H6/H7):** vetor somado na camada 6, com norma igual à mediana de ‖h‖, α = 1, 7 sementes de Bach × 2 amostras, continuações de 120 tokens relidas sem steering. Progresso em direção a Chopin: nenhum 0,39; aleatório 0,43; centrado 0,68. Centrado > aleatório em 7 de 7 sementes (Wilcoxon p = 0,016). **H6 confirmada.** Caminho: t = 0 → 0,28; t = 0,5 → 0,34; t = 1 → 0,69. Monótono (H7), mas não linear: o ponto médio do vetor fica perto de Bach. Repetição de trigramas baixa em todas as condições (≤ 4%).
- **F6 (controles):** transpor ±2 ou ±5 semitons desloca a peça em 0,02–0,03, contra 0,54 de distância média da peça ao próprio centróide e 0,94 entre centróides. O "estilo" medido **não é tonalidade**; só 12% das peças trocam de centróide mais próximo. O número de peças não correlaciona com a distância bruta à média (ρ = −0,11) nem com a dispersão (ρ ≈ 0); o z de originalidade cresce com n por construção, então o ensaio deve usar a distância bruta.
- **Metadados:** a verificação web por subagente foi bloqueada (Wikipedia e IMSLP fora da lista de domínios); só Hitz foi confirmado. `fronteira` recalculada pela regra mecânica. Os valores seguem como "conhecimento geral (verificar)".

Próximos passos: passada 2 (janela a 1/6) para medir a variação dentro da obra (o estilo interno de Meyer) e reforçar a média por peça; REPORTs por frente; figuras para a apresentação; revisão independente.

## 2026-11-08, 00:00 — passada 2 concluída; análises refeitas com 2 janelas por peça

Cada peça agora é a média de duas janelas (o meio e 1/6). As métricas da passada 1 estão guardadas em `metrics_passada1.json`, em cada pasta. **Decisão:** os números finais do ensaio são os de 2 janelas. Configuração inalterada: camada 6, com média.

- F2: acurácia balanceada de 0,35 (antes 0,30); estabilidade de 0,83.
- F3: H1, Mantel ρ = 0,50 (p < 0,001). H2: nacionalidade ρ = 0,08 (p = 0,02), que cai para 0,04 (p = 0,12) ao controlar a época. Distorção da PCA: 0,76. PC1 × ano de nascimento: ρ = 0,53, então a figura passou a dizer "acompanha, em parte, a cronologia". A maioria dos vizinhos mais próximos se manteve, mas alguns mudaram: Bach → Scarlatti (antes Handel) e Chopin → Grieg (antes Scriabin). Ver `vizinhos.csv`; os pares de vizinho mais próximo são instáveis e devem ser citados com cautela. Tico-Tico: C. L. Johnson, J. Scott, Nazareth, Czerny, Joplin.
- F4: R² do compositor = 0,28 (nulo 0,02); 65% das peças ficam mais perto de outro centróide; o compositor pesa mais que o gênero (R² de 0,32 contra 0,16 nas mesmas 1.053 peças com gênero identificado).
- F4b (estilo interno da obra, Meyer): distância entre janelas da **mesma peça** = 0,43; entre peças do mesmo compositor = 0,79; entre compositores = 1,01. A peça explica 78% da variância entre janelas, e o compositor 22%. Cada obra tem identidade própria forte; o compositor é um agrupamento mais frouxo dessas identidades.
- F5: contínuo (razão 1,77, contra p95 do nulo de 2,31). A divisão em 2 grupos é estável (ARI = 0,78), com o mesmo bloco pré-romântico {Bach, Handel, Scarlatti, Haydn, Mozart, Beethoven, Hummel}.
- F6 e F7 usaram os centróides da passada 1, com a mesma configuração. Não foram refeitos: a direção Bach → Chopin quase não muda.
- Cuidados levantados na revisão dos REPORTs: (1) em F7, progresso de 0,68 é projeção no eixo Bach → Chopin, não "chegar a Chopin"; a distância ao centróide de Chopin segue alta (cerca de 0,93). (2) t = 0,5 fica abaixo da continuação sem steering. (3) A monotonia em α só tem o piloto (3 sementes).

### Pendências para as próximas rodadas (em ordem)

1. **F7:** varredura de α ∈ {0; 0,25; 0,5; 1; 1,5} com vetor centrado e aleatório, 7 sementes (testa a monotonia de H6 e acha a faixa de quebra pela taxa de repetição); par inverso Chopin → Bach; exemplo ilustrativo Tico-Tico + Nazareth. Comandos de até 10 min.
2. **F4b:** nulo para a comparação mesma peça × mesmo compositor (permutar janelas entre peças do mesmo compositor) e IC bootstrap.
3. **Revisão independente** (subagente que só vê REPORTs, figuras e números) e correções.
4. **RESULTADOS.md:** conclusões por hipótese H1–H7, figuras candidatas para a apresentação e limitações.

## 2026-11-08, 00:40 — rodada autônoma 1

Ambiente intacto: dados, modelo e as 4.368 janelas extraídas. O modelo do Thiago não apareceu; seguimos com o AMT, como decidido.

- **F7, varredura de α** (Bach → Chopin, 7 sementes, 1 amostra cada; centróides com 2 janelas). Progresso com o vetor centrado: α = 0 → 0,38; 0,25 → 0,47; 0,5 → 0,59; 1 → 0,68; 1,5 → 0,76. A distância ao centróide de Chopin cai de 1,18 para 0,85. Com o vetor aleatório, o progresso fica plano (0,38–0,47). Repetição de trigramas ≤ 6% em tudo: **sem quebra até α = 1,5**. **H6 confirmada** com 7 sementes; a monotonia deixa de depender só do piloto.
- **F7, par inverso Chopin → Bach** (7 sementes): centrado 0,46 contra nenhum 0,33 e aleatório 0,29. Centrado > ambos em 7 de 7 sementes (p = 0,016). **Efeito assimétrico:** +0,14 contra +0,29 no sentido Bach → Chopin. No caminho, o vetor puro de Chopin (t = 0) puxa de volta para Chopin (0,19), e o ponto médio dá 0,41. Nos dois sentidos, a mistura meio a meio cai mais para o lado de Bach: o vetor de Bach "domina" a mistura.
- **Decisão:** o exemplo ilustrativo de steering com o Tico-Tico fica de fora. O Abreu não tem centróide (1 peça) e a posição do Tico-Tico no mapa já cumpre o papel ilustrativo. Economiza tempo de CPU e de revisão.
- **F4b, robustez:** em 100% dos compositores, as janelas da mesma peça ficam mais perto entre si do que de outras peças do mesmo compositor. Diferença média de 0,33 (IC95% 0,29–0,36).
- Ressalvas da revisão do REPORT da F7: a monotonia em α vale na média, mas só 4 de 7 sementes são individualmente monótonas; em α = 0,25 a vantagem sobre o aleatório ainda é fraca (5 de 7, p = 0,08). No par inverso, as condições "nenhum" e "aleatório" repetem mais (12% de trigramas repetidos), o que pode influir no progresso medido. Novas figuras: `steering_alfa.png` e `steering_dois_sentidos.png`.

## 2026-11-08, 06:30 — rodada autônoma 2

- **F6 refeita com a base de 2 janelas** (a versão anterior ficou em `*_passada1.*`). Transposição: deslocamento de 0,022 (±2 semitons) e 0,027 (±5), contra 0,93 entre centróides; em 9% dos casos o centróide mais próximo muda. Tamanho amostral: sem relação com a distância bruta (ρ = −0,12) nem com a dispersão (ρ = 0,04).
- **Robustez entre representações** (`F6_controles/secundaria.py`). H1 vale em todas: camada 6 média 0,51; camada 5 média 0,49; camada 12 média 0,42; camada 6 último token 0,41, todas com p = 0,001. A nacionalidade parcial fica entre 0,01 e 0,04 em todas. R² do compositor: 0,28 / 0,26 / 0,22 / 0,12. O bloco pré-romântico aparece em todas; nas camadas 12 e com último token, vem com intrusos. **Decisão:** as conclusões H1, H2, H3 e H5 não dependem da escolha fina da representação. O número exato do R² depende.
- **Tabela de validade** escrita em `analysis/F6_controles/VALIDADE.md`: 12 afirmações classificadas em sobrevive, enfraquece ou cai, mais o que nenhum controle cobre (pianista e gravação, modelo treinado no Lakh, poucos barrocos e clássicos).
- O dendrograma da F5 agora distingue J. Scott de C. Scott. A F5 foi refeita; números inalterados.

## Backlog do trabalho contínuo (2026-11-08, 07:10 → 13:00)

Pedido do Tomaz: trabalho contínuo, com leitura, escrita e revisão delegadas a subagentes baratos. Marque [x] ao concluir.

- [x] B1. Passada 3 de extração (janela a 5/6), em segundo plano, para 3 janelas por peça.
- [x] B2. Revisão independente (F9): um subagente confere REPORTs, VALIDADE e DIARIO contra os metrics e CSVs.
- [x] B3. Expectativa (Meyer): surpresa média do modelo (perda) por compositor e período, a partir da perda já salva por janela.
- [x] B4. Corrigir o que a revisão apontar.
- [x] B5. Refazer F2–F5 com 3 janelas, se a B1 terminar; registrar a estabilidade.
- [x] B6. RESULTADOS.md: conclusões por hipótese, números finais e limitações.
- [x] B7. APRESENTACAO.md: roteiro slide a slide (mensagem, figura, número, fala), para o grupo montar o deck às 13h.
- [x] B8. Revisão final de RESULTADOS e APRESENTACAO por um subagente independente.

## 2026-11-08, ~08:00 — errata da revisão independente (B4)

- F6/REPORT: texto na base da passada 1 (n×dist −0,11; refs 0,942/0,542; "não foi refeita") → números atuais de `metrics.json` (2 janelas: −0,116; z 0,461; dispersão 0,043; refs 0,9315/0,4938); percentuais do deslocamento 4,5–5,4% e 2,4–2,9%.
- F6/REPORT e VALIDADE: "transposição refeita com 2 janelas" → a transposição usa só a janela do meio de 45 peças (1 janela); só as referências e os centróides são de 2 janelas.
- F6/VALIDADE e DIARIO 22:40: "12% / 9% das peças trocam de centróide" → são linhas: 9,4% das linhas peça × transposição (17 de 180) e 29% das peças (13 de 45) em ao menos uma transposição; 12,2% (22 de 180) na passada 1.
- F3/REPORT, VALIDADE: "Satie ↔ Rebikov" → Satie → Rebikov, não mútuo (vizinho de Rebikov: Scharwenka, 0,267).
- F3/REPORT, DIARIO 00:00: PC1 × ano ρ = 0,53 → 0,525 (PC2 × ano 0,26).
- F4/REPORT, DIARIO 00:00: "a peça explica 78%, o compositor 22%" → R² bruto 0,78 com nulo de 0,50 por construção (2 janelas por peça), corrigido 0,57; compositor por janela 0,224 com nulo 0,013, corrigido 0,214; os dois não são comparáveis. Resultado robusto mantido: 52 de 52 compositores com janelas da mesma peça mais próximas (diferença 0,33, IC95% 0,29–0,36), confundido com a gravação/arquivo. "Identidade própria forte" retirado.
- F4/REPORT: lista dos cinco mais espalhados depende de empate (Schubert 0,8706 vs Mendelssohn 0,8709).
- VALIDADE linha 1: "p = 0,001" → p = 0,0002 (Mantel, 5.000 permutações, F3) ou ≤ 0,001 (1.000 permutações, `secundaria.py`).
- VALIDADE linha 2: "nacionalidade não organiza o mapa" → sem evidência de efeito (ρ parcial 0,04, p = 0,12; ausência de evidência, pouca potência).
- VALIDADE linha 4: "H4 refutada" → "não se confirma" (como na F4).
- VALIDADE linha 8: Tico-Tico "estável" → só os 3 primeiros vizinhos; 4º e 5º mudam e a distância a Nazareth vai de 0,546 para 0,488.
- VALIDADE linha 12: "separa estilo e não tonalidade / Sobrevive" → deslocamento pequeno em 45 peças, 1 janela, sem nulo nem IC; 13 de 45 peças trocam de centróide; veredito "Enfraquece".
- VALIDADE linha 1/3/6 e DIARIO 06:30: "H1, H2, H3, H5 não dependem da representação" → H1, H2 e o contínuo se mantêm; o R² de H3 varia (0,12–0,28) e o bloco de H5 ganha intrusos nas camadas 12 e com último token.
- VALIDADE linhas 5, 9, 10: redação de "identidade própria forte", "desloca a música em direção a ele" e "mistura se comporta como Bach" suavizada (efeito no eixo e no modelo usados; observação descritiva sem teste).
- F7/REPORT: tabela do par inverso comparava bases diferentes sem aviso → cabeçalhos marcam 1 janela (forte, n = 14) vs 2 janelas (inverso, n = 7); assimetria e "Bach domina" são observações descritivas, sem teste.
- F7/REPORT: "repetição de trigramas ≤ 4% em todas" (e DIARIO 00:40 "≤ 6% em tudo") → médias 1,5–4,1% no forte (nenhum 4,14%); máximos por continuação 28,9% (forte), 23,7% (varredura), 39,5% (inverso); aleatório α = 1,5 tem média 6,4%.
- F7/REPORT: "monótono em α" → a média cresce, mas por semente só 4 de 7 são monótonas; "sem quebra até α = 1,5" → sem aumento sistemático da repetição de trigramas (única medida de degeneração).
- Não aplicado: DIARIO 21:20 (51 compositores / 2.184 peças vs 52 / 2.183), por ser entrada antiga e fora dos arquivos editáveis.

## 2026-11-08, 08:10 — B1 e B5: passada 3 e teste de estabilidade com 3 janelas

- Passada 3 concluída: janela a 5/6 de cada peça, 2.184 arquivos, 55 min.
- **Decisão:** os números principais continuam sendo os de 2 janelas, base do RESULTADOS e do roteiro. A base de 3 janelas fica como teste de estabilidade, em `analysis/F6_controles/metrics_3janelas.json` e `vizinhos_3janelas.csv`. Os arquivos das frentes F2–F5 foram mantidos em 2 janelas.
- **Com 3 janelas:**
  - F2 escolhe de novo a camada 6 com média (acurácia 0,37; estabilidade 0,85).
  - H1: Mantel ρ = 0,51 (p = 0,0002).
  - Nacionalidade parcial: ρ = 0,04 (p = 0,11).
  - R² do compositor: 0,30 (nulo 0,02); sobreposição de 64%.
  - Gênero × compositor: R² de 0,18 contra 0,34.
  - Contínuo: razão 1,73, contra p95 do nulo de 2,37.
  - Tico-Tico: mesmos 3 vizinhos (Johnson, J. Scott, Nazareth).
  - Única mudança: o bloco k = 2 ganha Mendelssohn e Victoria (ARI 0,75). O núcleo pré-romântico se mantém, mas a fronteira do bloco depende da amostra.
- Conclusão: tudo o que o RESULTADOS afirma se mantém ou fica um pouco mais forte com mais janelas.

## 2026-11-08, 08:20 — B8 e verificação de metadados

- **B8:** revisão final independente de RESULTADOS.md e APRESENTACAO.md. Foram 30 ajustes, quase todos de redação: avisos de figura obsoletos, exageros, mistura de bases em F7 e atribuições a Meyer que não podemos conferir. O registro está em REVISAO_FINAL.md. Também foi corrigida a descrição de `h0_barras.png`: a maior parte das fusões fica **abaixo** da faixa do nulo e só a última barra fica dentro.
- **Metadados:** o WebFetch funciona quando chamado pelo coordenador (nos subagentes em segundo plano ficava esperando permissão). Conferi no IMSLP os 9 compositores de baixa confiança. Só Teilman estava errado: nasceu em 1845 e é **norueguês**, não dinamarquês. Os outros 8 confirmados, com URL na coluna `fonte`. Gurlitt aparece no IMSLP como alemão e dinamarquês; mantido Alemão.
- F3 refeita com a correção (2 janelas): H1 ρ = 0,505; nacionalidade ρ = 0,083 (p = 0,019) e, controlando a época, ρ = 0,041 (p = 0,111). Números atualizados nos documentos. Conclusões inalteradas.
- README: corrigido o modelo dos resultados (AMT, treinado no Lakh), não "treinado no GiantMIDI".

## 2026-11-08, 08:35 — material extra para a apresentação

- Diagramas dos slides 2 e 10: `analysis/figs_apresentacao/pipeline.png` (o fluxo do trabalho para leigos) e `meyer_niveis.png` (os níveis de estilo e o achado de cada um). O APRESENTACAO.md já aponta para eles.
- Exemplos em MIDI: `analysis/F7_deslocamento/exemplos_midi/`. Semente da Sinfonia BWV 796 de Bach, continuada sem steering, com vetor de Chopin em α = 1 e com α = 1,5. São ilustração (1 semente, 1 amostra), não evidência. Observação a conferir ouvindo: as versões com Chopin saíram 2 a 3 vezes mais lentas (32 s e 24 s, contra 10 s, para as mesmas 130 notas). Pode ser acaso. Se for sistemático, é um caminho interessante, mas fora do escopo agora.

## 2026-11-08, 08:45 — descritores independentes do steering (princípio 7 do plano)

`analysis/F7_deslocamento/descritores.py`, com 7 sementes de Bach × 2 amostras × {nenhum, aleatório, centrado de Chopin α = 1}, descritores só da continuação. O vetor de Chopin alonga as notas (0,30 → 0,65 s; Chopin 0,63; 7/7) e aumenta a polifonia (2,4 → 3,0), na direção de Chopin. Mas reduz as notas por segundo (9,0 → 4,8; 7/7) e a altura média, **contra** a direção de Chopin. A lentidão dos exemplos MIDI é sistemática e vem de notas mais longas e espaçadas. **Decisão:** relatar como "o vetor muda a textura de forma parcialmente compatível com Chopin". RESULTADOS (Q4) e o slide 7 foram atualizados.

## 2026-11-08, 08:55 — steering em outros pares (generalização de H6)

Três pares novos, cada um com 7 sementes, 1 amostra e α = 1: Haydn → Mozart (próximos), Mozart → Debussy (distantes) e Joplin → Chopin (intermediários).
- Mozart → Debussy: o centrado supera o aleatório em 6 de 7 sementes (p = 0,031).
- Joplin → Chopin: 5 de 7 (p = 0,69), sem efeito claro.
- Haydn → Mozart: não interpretável. A distância entre os centróides é de 0,10, então o eixo fica mal definido e o progresso sai de 0–1.

**Decisão:** H6 passa a "vale em 3 de 4 direções interpretáveis, todas entre compositores distantes", com veredito "enfraquece" na VALIDADE (linha 9b). Resumo em `pares_resumo.csv`; RESULTADOS, REPORT da F7 e slide 7 atualizados.

## 2026-11-08, 08:45 — backlog concluído

Itens B1–B8 concluídos, mais os extras: diagramas, exemplos MIDI, descritores independentes e 3 pares novos de steering. O que fica para o grupo decidir às 13h:
- **Slide 7:** o título e a fala ainda giram em torno de Bach → Chopin; o campo "cuidado" e a figura de apoio já refletem os 4 pares.
- **Metadados:** os compositores conhecidos seguem sem URL de fonte. Só os 9 de baixa confiança foram conferidos no IMSLP.
- **Exemplos MIDI:** ouvir antes de usar.
- **Deck:** montar a partir do APRESENTACAO.md.

## 2026-11-08, 09:15 — Plano 2: resultados

- **A (superfície, F9).** Os descritores simbólicos simples explicam 50% da variância das representações. Mas o mapa só de descritores acompanha a época bem menos (Mantel 0,20 contra 0,50), e a RSA modelo × descritores é 0,64. Sem os descritores, a cronologia continua (0,34) e a sonda cai pouco (0,35 → 0,31). Surpresa × época: 0,51 → 0,41 com descritores controlados (p = 0,002). **O modelo sabe mais que estatística de superfície.**
- **B (gênero, F10).** Sem o gênero do título, a cronologia continua (0,38). O bloco pré-romântico segue no mesmo ramo, mas o corte em 2 grupos deixa de isolá-lo.
- **C1 (F11).** Resíduos de "à frente ou atrás do tempo": 37 de 52 com IC (só da amostragem de peças) que exclui zero. O padrão: ragtime e clássicos soam "mais antigos" que a data; o romantismo tardio, "mais moderno". **Decisão:** usar só como ilustração, porque o IC não inclui a incerteza da reta e da PCA.
- **C2 (finais, F12).** H13 cai: efeito de cerca de 1% e de sinal oposto entre períodos.
- **C3 (fio brasileiro, F13).** Gêneros de Nazareth verificados em fontes (IMSLP, Musica Brasilis, Nazareth 150 anos). As 4 valsas ficam longe do ragtime e perto de Chopin, e os 8 tangos e polcas, o contrário: separação completa (p = 0,002). As valsas de Joplin e Johnson também ficam mais perto de Chopin que os 79 rags (p = 0,0003). **Para o modelo, a "valsa" atravessa culturas.** Ressalva: o compasso 3/4 pode ser o que ele capta.
- **D.** Explorador interativo publicado como artifact (https://claude.ai/artifact/NeP4zc74AncnZsXsZuLvvo). Figuras novas: `F9_superficie/figs/controles_cronologia.png`, `F13_brasil/figs/valsas.png`, `F4_nuvens/figs/nuvens_pecas.png`, `F11_tempo/figs/tempo_vs_mapa.png`.
