"""Gera pipeline.png (slide 2) e meyer_niveis.png (slide 10). Sem modelos."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.dirname(os.path.abspath(__file__))
INK = "#222222"
BLUE = "#dbe8f5"; BLUE_E = "#3b6ea5"
GREEN = "#e1f0e0"; GREEN_E = "#4a8a49"
ORANGE = "#fbe9d0"; ORANGE_E = "#c0762a"
plt.rcParams["font.family"] = "DejaVu Sans"


def canvas():
    fig = plt.figure(figsize=(16, 9), dpi=150, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc, ec, fs=14, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc=fc, ec=ec, lw=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK,
            fontweight="bold" if bold else "normal", linespacing=1.3)


def arrow(ax, p, q, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=22, lw=2, color=color,
                                 shrinkA=0, shrinkB=0))


# ---------- pipeline ----------
fig, ax = canvas()
ax.text(8, 8.35, "Do acervo de piano à impressão digital de cada compositor", ha="center",
        fontsize=20, fontweight="bold", color=INK)
steps = [
    "2.183 peças\nde piano\n(GiantMIDI,\n52 compositores)",
    "Trechos de\n~340 notas\n(2 por peça)",
    "Modelo que prevê\na próxima nota\n(AMT, treinado\nem outro acervo)",
    "\"Impressão\ndigital\" de cada\ntrecho (média da\ncamada 6,\n768 números)",
    "Média por\ncompositor =\nvetor do\ncompositor",
]
w, h, gap, x0, y0 = 2.0, 3.2, 0.5, 0.35, 2.9
for i, t in enumerate(steps):
    x = x0 + i * (w + gap)
    box(ax, x, y0, w, h, t, BLUE, BLUE_E, fs=14)
    if i < len(steps) - 1:
        arrow(ax, (x + w + 0.04, y0 + h / 2), (x + w + gap - 0.04, y0 + h / 2))
# saídas
xo, wo, ho = 13.55, 2.1, 0.95
ys = [6.0, 4.6, 3.2, 1.8]
labels = ["Mapa", "Nuvens", "Forma", "Andar no\nespaço"]
xl = x0 + 4 * (w + gap) + w
for lab, y in zip(labels, ys):
    box(ax, xo, y, wo, ho, lab, GREEN, GREEN_E, fs=15, bold=True)
    arrow(ax, (xl + 0.04, y0 + h / 2), (xo - 0.04, y + ho / 2), color=GREEN_E)
ax.text(xo + wo / 2, 7.25, "Saídas", ha="center", fontsize=15, fontweight="bold", color=GREEN_E)
ax.text(8, 0.9, "Daqui em diante tudo é geometria: perto e longe, do ponto de vista do modelo.",
        ha="center", fontsize=15, color=INK, style="italic")
ax.text(8, 0.4, "O modelo foi treinado no Lakh MIDI, não em música clássica.",
        ha="center", fontsize=13, color="#555555")
fig.savefig(os.path.join(OUT, "pipeline.png"), facecolor="white")
plt.close(fig)

# ---------- níveis de Meyer ----------
fig, ax = canvas()
ax.text(8, 8.4, "Níveis de estilo e o que o modelo mostra em cada um", ha="center",
        fontsize=20, fontweight="bold", color=INK)
ax.text(2.6, 7.6, "Nível", ha="center", fontsize=14, fontweight="bold", color="#555555")
ax.text(10.1, 7.6, "Achado no espaço do modelo", ha="center", fontsize=14,
        fontweight="bold", color="#555555")
levels = [
    ("Época\n(dialeto)", BLUE, BLUE_E,
     "A distância entre compositores cresce com a diferença de época\n"
     "(ρ = 0,505): relação moderada, e um bloco de 7 pré-românticos\n"
     "(Bach a Beethoven) se separa dos outros 45."),
    ("Compositor\n(idioma)", GREEN, GREEN_E,
     "O compositor explica 28% da variação entre peças\n"
     "(R² = 0,275): é uma nuvem que se sobrepõe às vizinhas,\n"
     "não um ponto."),
    ("Obra", ORANGE, ORANGE_E,
     "Trechos da mesma peça ficam mais próximos entre si\n"
     "em 52 de 52 compositores. Indício fraco: a medida\n"
     "mistura a obra com a gravação e o arquivo MIDI."),
]
bh, bw = 1.6, 3.4
for i, (name, fc, ec, txt) in enumerate(levels):
    y = 5.6 - i * 1.95
    xb = 0.9 + i * 0.5          # degraus
    box(ax, xb, y, bw, bh, name, fc, ec, fs=17, bold=True)
    ax.plot([xb + bw + 0.05, 6.55], [y + bh / 2] * 2, color=ec, lw=2, ls=(0, (3, 3)))
    ax.add_patch(FancyBboxPatch((6.6, y), 8.9, bh, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc="white", ec=ec, lw=2))
    ax.text(6.85, y + bh / 2, txt, ha="left", va="center", fontsize=13.5, color=INK, linespacing=1.4)
# seta lateral: do geral ao particular
arrow(ax, (0.45, 7.1), (0.45, 1.85), color="#777777")
ax.text(0.25, 4.5, "do mais geral ao mais particular", rotation=90, ha="center", va="center",
        fontsize=12, color="#555555")
ax.text(8, 1.0, "Leitura interpretativa com a ideia geral de estilo em níveis; não prova que o modelo "
        "\"entende\" estilo.", ha="center", fontsize=13, style="italic", color=INK)
ax.text(8, 0.4, "Medido num modelo treinado no Lakh MIDI, que só vê notas e tempos.",
        ha="center", fontsize=12.5, color="#555555")
fig.savefig(os.path.join(OUT, "meyer_niveis.png"), facecolor="white")
plt.close(fig)
