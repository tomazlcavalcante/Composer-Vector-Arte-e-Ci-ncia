# F6 — Controles

## Pergunta
O que medimos é efeito de tamanho amostral ou de tonalidade/registro?

## Hipótese registrada
Nenhuma hipótese própria na seção 5 do PLANO.md. A frente serve de controle para F3 a F5. Expectativa implícita: o "estilo" medido não deve mudar com transposição pequena nem com o número de peças.

## Configuração
- Tamanho amostral: Spearman entre nº de peças e (a) distância à média geral, (b) z de originalidade, (c) dispersão (F3 e F4, passada 2: 2 janelas por peça).
- Transposição: 45 peças (sorteadas, `random_state=0`), transpostas ±2 e ±5 semitons (180 linhas em `transposicao.csv`). **Só a janela do meio** de cada peça é transposta e relida pelo modelo (uma janela, não as 2); mede-se o deslocamento cosseno e se o centróide mais próximo muda. Os deslocamentos são os mesmos da passada 1 (diferença máxima por linha 0,0008); o que usa 2 janelas são as referências e os centróides em que se busca o mais próximo. O vetor transposto é de 1 janela, comparado a centróides de 2 janelas.
- Camada 6, pooling média.
- **Base:** `metrics.json` e `transposicao.csv` são da passada 2 (centróides e referências com 2 janelas por peça). A passada 1 (1 janela) está em `metrics_passada1.json` e `transposicao_passada1.csv`.

## Resultado
- n × distância à média geral: ρ = −0,116.
- n × z de originalidade: ρ = 0,461.
- n × dispersão: ρ = 0,043.
- Deslocamento médio por transposição: ±2 semitons 0,0223 (dp 0,0129, 90 linhas); ±5 semitons 0,0269 (dp 0,0114, 90 linhas). Máximo observado 0,074.
- Referências (2 janelas): distância média entre centróides 0,9315; distância média da peça ao próprio centróide 0,4938.
- O centróide mais próximo muda em 9,4% das linhas peça × transposição (17 de 180) e em 29% das peças (13 de 45) em pelo menos uma transposição. Na passada 1 eram 12,2% das linhas (22 de 180); 23 das 180 linhas mudam de resposta entre as duas bases, então o percentual não é estável.

## Comparação com o nulo
Não há nulo formal. As referências são as distâncias reais: o deslocamento por transposição (0,022 a 0,027) é cerca de 4,5 a 5,4% da distância peça-centróide (0,494) e 2,4 a 2,9% da distância entre centróides (0,9315).

## O que não se pode concluir
- O z de originalidade cresce com n por construção (ρ = 0,46). Usar a distância bruta (ρ = −0,11), não o z, no ensaio.
- Transpor ±2 e ±5 desloca pouco, então a tonalidade sozinha não explica o mapa. Não prova que o modelo ignora tonalidade: só mostra que mover uma peça inteira de tom, mantendo o resto, quase não muda o vetor.
- Só 45 peças, 4 transposições, só a janela do meio de cada peça (1 janela). Sem IC.
- Os 9,4% são linhas (peça × transposição); por peça, 29% (13 de 45) trocam de centróide em ao menos uma transposição. Isso é bastante: o teste não mostra que a tonalidade é irrelevante para o mapa.
- Não foram feitos controles de andamento, dinâmica nem linha de base simbólica. O tokenizador não vê andamento nem pedal.
- A "tabela de validade" (sobrevive / enfraquece / cai) para F3–F5, prevista no README da frente, não foi gerada aqui.

## Figuras
Nenhuma.

## Ideias fora do escopo
- Controle de andamento (esticar o tempo) e de dinâmica.
- Linha de base simbólica (histograma de intervalos, duração, densidade) para comparar com o espaço do modelo.
- Mais transposições (±1 a ±6) e mais peças, com IC.
- Montar a tabela de validade.
