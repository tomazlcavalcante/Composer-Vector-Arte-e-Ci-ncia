# F1 — Seleção e metadados

**Pergunta:** quem entra no mapa, e com que rótulos históricos?

- Compositores com ≥ 20 peças, chave 'Sobrenome, Nome'; **excluir os contemporâneos de YouTube** (ex.: Carbajo, Simpson, Zhang) e registrar a lista excluída.
- Para cada um: nascimento, morte, nacionalidade (verificados à mão, com fonte por campo).
- Período pela regra mecânica: nascimento + 30 anos, cortes em 1750 / 1820 / 1900 → Barroco / Clássico / Romântico / Moderno; coluna `fronteira` para casos ambíguos.
- `pieces.csv`: gênero por palavra-chave do título (sonata, estudo, valsa, mazurca, noturno, prelúdio, fuga, rag, variações, …).

**Saída:** `../data/metadata_curated.csv`, `../data/pieces.csv`, `REPORT.md`.
