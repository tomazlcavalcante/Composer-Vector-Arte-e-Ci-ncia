# F6 — Controles

## Pergunta
O que medimos é efeito de tamanho amostral ou de tonalidade/registro?

## Hipótese registrada
Nenhuma hipótese própria na seção 5 do PLANO.md. A frente serve de controle para F3 a F5. Expectativa implícita: o "estilo" medido não deve mudar com transposição pequena nem com o número de peças.

## Configuração
- Tamanho amostral: Spearman entre nº de peças e (a) distância à média geral, (b) z de originalidade, (c) dispersão (F3 e F4).
- Transposição: 45 peças (sorteadas, `random_state=0`), transpostas ±2 e ±5 semitons (180 linhas em `transposicao.csv`). A janela do meio é relida pelo modelo e mede-se o deslocamento cosseno e se o centróide mais próximo muda.
- Camada 6, pooling média.

## Resultado
- n × distância à média geral: ρ = −0,11.
- n × z de originalidade: ρ = 0,46.
- n × dispersão: ρ = 0,004.
- Deslocamento médio por transposição: ±2 semitons 0,0223 (dp 0,0129, 90 linhas); ±5 semitons 0,0269 (dp 0,0114, 90 linhas). Máximo observado 0,074.
- Referências: distância média entre centróides 0,942; distância média da peça ao próprio centróide 0,542.
- O centróide mais próximo muda em 12,2% das linhas (22 de 180).

## Comparação com o nulo
Não há nulo formal. As referências são as distâncias reais: o deslocamento por transposição (0,02 a 0,03) é cerca de 4 a 5% da distância peça-centróide (0,542) e 2 a 3% da distância entre centróides (0,942).

## O que não se pode concluir
- O z de originalidade cresce com n por construção (ρ = 0,46). Usar a distância bruta (ρ = −0,11), não o z, no ensaio.
- Transpor ±2 e ±5 desloca pouco, então a tonalidade sozinha não explica o mapa. Não prova que o modelo ignora tonalidade: só mostra que mover uma peça inteira de tom, mantendo o resto, quase não muda o vetor.
- Só 45 peças, 4 transposições, uma janela cada. Sem IC.
- Os 12,2% são linhas (peça × transposição), não 12% de peças.
- Não foram feitos controles de andamento, dinâmica nem linha de base simbólica. O tokenizador não vê andamento nem pedal.
- A "tabela de validade" (sobrevive / enfraquece / cai) para F3–F5, prevista no README da frente, não foi gerada aqui.

## Figuras
Nenhuma.

## Ideias fora do escopo
- Controle de andamento (esticar o tempo) e de dinâmica.
- Linha de base simbólica (histograma de intervalos, duração, densidade) para comparar com o espaço do modelo.
- Mais transposições (±1 a ±6) e mais peças, com IC.
- Montar a tabela de validade.
