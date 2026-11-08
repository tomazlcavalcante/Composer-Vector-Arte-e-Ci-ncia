# Plano 2: amadurecer os resultados (08/11, 09:00 → 13:00)

Ponto de partida: RESULTADOS.md. Os achados mais interessantes são três:
1. Um modelo treinado em música popular (Lakh), sem nenhum rótulo de compositor, organiza os compositores clássicos de forma parcialmente cronológica (ρ = 0,50), e não por nacionalidade.
2. O Tico-Tico cai ao lado do ragtime e de Nazareth.
3. O vetor de um compositor muda a textura da música gerada entre estilos distantes.

A maior fraqueza ainda aberta é não saber se tudo isso é só **estatística de superfície** (densidade de notas, registro, duração) ou **gênero** (fugas antes, noturnos depois). O Plano 2 ataca essa pergunta primeiro e depois transforma os resultados em visualizações que contam a história.

Todas as hipóteses abaixo ficam registradas **antes** dos resultados. Base: camada 6, média, 2 janelas por peça.

## Bloco A. O modelo sabe mais que estatística de superfície? (prioridade máxima)

- **A1. Descritores por janela** (sem o modelo): notas/s, altura média, desvio e extensão da altura, duração média, polifonia, intervalos melódicos (histograma), histograma de classes de altura (12). Para as 4.366 janelas.
- **A2. Mapa só com descritores:** centróides por compositor no espaço dos descritores padronizados.
  - *H8:* o mapa de descritores também correlaciona com a época, mas menos que o do modelo (Mantel menor).
  - *H9:* a correlação entre as duas matrizes de distância (RSA) é moderada, abaixo de 0,7. O modelo não se reduz aos descritores.
- **A3. Controle por superfície:** regredir os descritores para fora das representações (resíduos) e refazer H1 (Mantel), H3 (R²) e a acurácia da sonda.
  - *H10:* a cronologia sobrevive a esse controle, com ρ > 0,3.
- **A4. Expectativa controlada:** refazer F8 (surpresa × época) com correlação parcial, controlando notas/s, polifonia e duração.
  - *H11:* a correlação surpresa × época cai, mas não some.

## Bloco B. É época ou é gênero?

- **B1.** Regredir o gênero da peça (one-hot pelo título; "outro" como categoria) para fora das representações e refazer H1 e o bloco pré-romântico.
  - *H12:* a cronologia sobrevive (ρ > 0,3) e o bloco pré-romântico continua estável.

## Bloco C. Relações novas para o ensaio

- **C1. "À frente ou atrás do seu tempo":** resíduo da posição no eixo cronológico do mapa (PC1) contra o ano de nascimento, com IC por bootstrap de peças. Lista dos compositores que soam, **para o modelo**, mais "antigos" ou mais "modernos" que a sua data. Só se reportam resíduos com IC que exclui zero.
- **C2. Finais de obra (estilo interno, Meyer):** a janela final (5/6) fica mais perto do centróide do próprio compositor, ou do período, que a inicial (1/6)?
  - *H13:* os finais são mais convencionais, isto é, mais próximos do centróide do período. Teste pareado por peça.
- **C3. O fio brasileiro:** dentro de Nazareth, os tangos e maxixes ficam mais perto do ragtime que as valsas?
  - *H14:* sim. Teste pareado por peça, n pequeno e tratado como exploratório. Onde fica o Villa-Lobos?

## Bloco D. Visualizações que contam a história

- **D1.** Explorador interativo (página HTML publicada como artifact): mapa dos 52 compositores com cor por período, nacionalidade ou surpresa. Ao passar o mouse aparecem datas, vizinhos e número de peças. Ao clicar, mostra a nuvem de peças do compositor, linhas para os vizinhos e a estrela do Tico-Tico. Inclui também as setas do steering.
- **D2.** Rede de vizinhos mútuos (k = 3), colorida por período.
- **D3.** "Linha do tempo × mapa": nascimento no eixo x e posição no eixo cronológico no y, com os resíduos de C1 destacados.
- **D4.** Mapa das 2.183 peças (nuvens sobrepostas), destacando 4 compositores.

## Bloco E. Síntese

- **E1.** Atualizar RESULTADOS, VALIDADE e APRESENTACAO com o que sobreviver.
- **E2.** Revisão independente final.
- **E3.** Cópia dos documentos e figuras na pasta `Projetos/Composer_Vector` do notebook.

## Divisão

Os subagentes baratos (sonnet) fazem A1, B1, C1–C3, D2–D4 e as revisões. O coordenador faz A2–A4 (dependem de A1), D1 (o artifact) e a integração. Cada item vira commit e uma linha no DIARIO.md.
