# Tabela de validade

Para cada afirmação principal, o veredito diante dos controles. **Sobrevive**: nenhum controle a ameaça. **Enfraquece**: vale, mas com ressalva. **Cai**: não se sustenta.

Base: camada 6, média, 2 janelas por peça, 52 compositores, 2.183 peças. Fontes: `metrics.json`, `metrics_secundaria.json` e `transposicao.csv` (nesta pasta) e os `metrics.json` de F3, F4, F5 e F7.

| # | Afirmação | Controles | Veredito |
|---|---|---|---|
| 1 | A distância entre compositores cresce com a diferença de época (H1, Mantel ρ = 0,50) | Permutação (p = 0,001). Vale em todas as representações testadas: camada 5 (0,49), camada 12 (0,42) e último token (0,41). Transposição desloca 0,02–0,03, contra 0,93 entre centróides | **Sobrevive** |
| 2 | A nacionalidade não organiza o mapa quando a época é controlada (H2) | Parcial ρ = 0,01–0,04 em todas as configurações. Ressalva: os metadados não foram verificados em fonte externa | **Sobrevive** (com a ressalva dos metadados) |
| 3 | O estilo é mais nuvem que ponto: o compositor explica cerca de 28% da variância entre peças, e 65% das peças ficam mais perto de outro centróide (H3) | Nulo de rótulos permutados (2%). R² de 0,26 na camada 5, 0,22 na camada 12 e 0,12 com último token: o valor depende da representação, mas é sempre uma minoria bem acima do nulo | **Sobrevive** (o número exato depende da representação) |
| 4 | O compositor pesa mais que o gênero da peça (H4 refutada) | Gênero por palavra-chave do título, em 1.053 peças: R² de 0,32 (compositor) contra 0,16 (gênero). R² não ajustado pelo número de grupos; gêneros por título são imprecisos | **Enfraquece** |
| 5 | Cada obra tem identidade própria forte: janelas da mesma peça são mais próximas entre si do que de outras peças do autor (Meyer, intra-opus) | Vale em 52 de 52 compositores; diferença de 0,33 (IC95% 0,29–0,36). Parte pode ser característica da gravação ou do arquivo, que é a mesma nas duas janelas | **Enfraquece** (confundido com a gravação) |
| 6 | O espaço é um contínuo, com um único corte estável: o bloco pré-romântico (Bach, Handel, Scarlatti, Haydn, Mozart, Beethoven, Hummel) contra o resto (H5) | Nulo gaussiano: sem lacuna anormal. ARI do k = 2 em bootstrap: 0,78. O mesmo bloco aparece nas camadas 5 e 6; nas camadas 12 e com último token, ele vem com intrusos (Victoria, ragtime). Grupos com k ≥ 3 são instáveis | **Sobrevive** para o contínuo e o bloco pré-romântico; **cai** para grupos mais finos |
| 7 | Vizinhos com sentido musical (Haydn–Mozart, Debussy–C. Scott, Satie–Rebikov, ragtime) | Vários pares mudam entre 1 e 2 janelas (ex.: Bach → Handel/Scarlatti, Chopin → Scriabin/Grieg). Pares individuais não têm teste | **Enfraquece**: usar como ilustração, não como resultado |
| 8 | Tico-Tico cai ao lado do ragtime e de Nazareth | Uma peça só, uma ilustração; estável entre 1 e 2 janelas | **Ilustração**, não resultado |
| 9 | Somar o vetor centrado de um compositor desloca a música gerada em direção a ele (H6) | Contra vetor aleatório de mesma norma e contra continuação sem steering: 7 de 7 sementes nos dois sentidos (p = 0,016); monótono em α na média. Medida relendo sem steering. Efeito parcial: a música não chega ao centróide do alvo | **Sobrevive** (como deslocamento parcial) |
| 10 | O caminho Bach → Chopin é monótono; a mistura meio a meio se comporta como Bach (H7) | Nos dois sentidos, mas com 7 sementes e um único par de compositores | **Enfraquece** (um par só) |
| 11 | "Originalidade" (distância à média geral) | O número de peças não correlaciona com a distância bruta (ρ = −0,12); o z de originalidade cresce com n por construção | Usar só a distância bruta |
| 12 | O modelo separa estilo e não tonalidade | Transposição de ±2 ou ±5 semitons: deslocamento de 0,02–0,03; em 9% das peças transpostas (contando cada transposição) o centróide mais próximo muda | **Sobrevive** |

**O que nenhum controle cobre:**
- **Pianista e gravação:** o GiantMIDI transcreve gravações do YouTube, e não separamos o intérprete do compositor.
- **Modelo:** o AMT foi treinado no Lakh MIDI, não em música clássica.
- **Amostra:** há poucos compositores barrocos e clássicos.
