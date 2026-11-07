# F2 — Escolha da representação (bloqueia F3–F7)

**Pergunta:** em que camada e com que pooling o modelo separa melhor, e de forma mais estável, a identidade do compositor?

**Proibido:** usar período ou nacionalidade.

Grade (versão de dois dias): camadas {2, 4, 6} × pooling {último, média}, espaço centrado, cosseno. Critérios: acurácia balanceada de regressão logística com divisão **por peça** (GroupKFold), razão entre/intra-compositor, estabilidade bootstrap dos centróides. Hipótese: camadas intermediárias ≥ camada 6.

**Saída:** configuração principal + secundária justificadas, `REPORT.md`.
