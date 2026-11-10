# Apresentação em LaTeX: Como um modelo de música organiza os compositores

Versão em Beamer do deck da apresentação de Artes e Ciência (IMPA Tech, novembro de 2026).

## O que tem aqui

```
apresentacao_latex/
├── main.tex          ← os slides (13 principais, agradecimento, 6 de reserva)
├── main.pdf          ← já compilado
├── figuras/          ← todas as figuras usadas nos slides (PNG)
└── html/
    ├── explorador.html      ← mapa interativo dos 52 compositores (abre offline)
    └── escuta/
        ├── index.html       ← trechos gerados para ouvir
        └── audio/           ← os 44 MP3 usados pela página
```

## Como compilar

Compila com **pdfLaTeX** (o padrão do Overleaf), **XeLaTeX** ou **LuaLaTeX**:

```
latexmk -pdf main.tex        # pdfLaTeX
latexmk -xelatex main.tex    # XeLaTeX
```

Fonte: com pdfLaTeX, usa o pacote `inter` se ele existir na instalação; com XeLaTeX ou LuaLaTeX, usa a fonte Inter do sistema, se estiver instalada. Sem a Inter, cai na sans padrão do LaTeX sem dar erro. O `main.pdf` incluído foi compilado com XeLaTeX e a Inter. A fonte é gratuita: https://rsms.me/inter/

## Notas do apresentador

As falas e os cuidados de cada slide estão em `\note{...}` dentro de cada frame. Para vê-las, descomente esta linha no começo de `main.tex`:

```
% \setbeameroption{show notes on second screen=right}
```

O PDF passa a ter o slide à esquerda e as notas à direita, para usar com o segundo monitor (por exemplo, no pdfpc).

## Os links do último slide

O slide 13 aponta para as duas páginas publicadas no GitHub Pages do repositório:

- Mapa interativo: https://tomazlcavalcante.github.io/Composer-Vector-Arte-e-Ci-ncia/apresentacao_latex/html/explorador.html
- Trechos para ouvir: https://tomazlcavalcante.github.io/Composer-Vector-Arte-e-Ci-ncia/apresentacao_latex/html/escuta/index.html

Funcionam em qualquer leitor de PDF com internet. As mesmas páginas estão na pasta `html/` para abrir sem internet, direto no navegador.

## Origem

Gerado a partir do repositório do grupo (`analysis/`). As figuras vêm de `F2`, `F3`, `F4`, `F5`, `F7`, `F8`, `F9`, `F11` e `F15`; as páginas HTML, de `D1_explorador` e `F18_escuta`.
