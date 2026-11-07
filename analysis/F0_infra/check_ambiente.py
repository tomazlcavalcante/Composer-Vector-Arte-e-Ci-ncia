"""Verifica se a máquina está pronta para o projeto. Uso:

    python analysis/F0_infra/check_ambiente.py [--checkpoint CAMINHO] [--midis PASTA]

Cada linha diz OK, AVISO ou FALHA. Nada aqui altera arquivos.
"""
import argparse
import importlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
TOK_CFG = ROOT / "analysis" / "data" / "tokenizer_config.json"
problems = []


def report(status, msg):
    print(f"[{status:5}] {msg}")
    if status == "FALHA":
        problems.append(msg)


ap = argparse.ArgumentParser()
ap.add_argument("--checkpoint", default=os.environ.get("CV_CHECKPOINT"))
ap.add_argument("--midis", default=os.environ.get("CV_MIDIS"))
args = ap.parse_args()

# 1. Python e GPU
report("OK" if sys.version_info >= (3, 10) else "AVISO", f"Python {sys.version.split()[0]}")
if shutil.which("nvidia-smi"):
    out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,memory.used", "--format=csv,noheader"],
                         capture_output=True, text=True).stdout.strip()
    report("OK", f"nvidia-smi: {out}")
else:
    report("FALHA", "nvidia-smi não encontrado (sem driver NVIDIA?)")

# 2. Pacotes e versões fixadas
expected = json.loads(TOK_CFG.read_text()) if TOK_CFG.exists() else {}
pins = {"miditok": expected.get("miditok_version"), "symusic": expected.get("symusic_version"),
        "tokenizers": expected.get("hf_tokenizers_version")}
for pkg in ["torch", "miditok", "symusic", "tokenizers", "numpy", "pandas", "scipy", "sklearn", "matplotlib", "ripser"]:
    try:
        mod = importlib.import_module(pkg)
        ver = getattr(mod, "__version__", "?")
        want = pins.get(pkg)
        if want and ver != want:
            report("FALHA", f"{pkg} {ver} (o tokenizador do treino foi salvo com {want})")
        else:
            report("OK", f"{pkg} {ver}")
    except Exception as e:  # noqa: BLE001
        report("FALHA", f"{pkg} não importa: {e}")

try:
    import torch
    if torch.cuda.is_available():
        report("OK", f"torch.cuda: {torch.cuda.get_device_name(0)}, CUDA {torch.version.cuda}")
        device = "cuda"
    else:
        report("FALHA", "torch não enxerga a GPU (torch.cuda.is_available() == False)")
        device = "cpu"
except Exception:
    device = None

# 3. Tokenizador
tokenizer = None
try:
    from miditok import REMI
    tokenizer = REMI(params=TOK_CFG)
    report("OK" if len(tokenizer) == 3000 else "AVISO", f"tokenizador carregado, vocabulário {len(tokenizer)}")
except Exception as e:  # noqa: BLE001
    report("FALHA", f"tokenizador não carrega: {e}")

# 4. Dados
pieces = []
if args.midis and Path(args.midis).is_dir():
    from analysis.common.data import list_pieces
    pieces = list_pieces(args.midis)
    n_comp = len({p.composer_key for p in pieces})
    report("OK" if len(pieces) > 7000 else "AVISO", f"{len(pieces)} MIDIs, {n_comp} compositores (esperado ≈ 7.236 / 1.787)")
else:
    report("FALHA", "pasta de MIDIs não informada ou inexistente (--midis ou CV_MIDIS)")

# 5. Checkpoint, perda e velocidade
if args.checkpoint and Path(args.checkpoint).is_file() and device and tokenizer is not None:
    from analysis.common.model import load_model, generate
    import torch.nn.functional as F
    model, ckpt = load_model(args.checkpoint, len(tokenizer), device)
    report("OK", f"checkpoint carregado (época {ckpt.get('epoch')}, best_val_loss {ckpt.get('best_val_loss', float('nan')):.4f})")
    if pieces:
        import random
        from analysis.common.data import fragments
        random.seed(0)
        losses = []
        for p in random.sample(pieces, min(60, len(pieces))):
            try:
                ids = tokenizer(p.path)[0].ids
            except Exception:  # noqa: BLE001
                continue
            for _, frag in fragments(ids):
                x = torch.tensor([frag[:-1]], device=device)
                y = torch.tensor([frag[1:]], device=device)
                with torch.no_grad():
                    losses.append(F.cross_entropy(model(x)[0].float(), y[0]).item())
                break
        if losses:
            m = sum(losses) / len(losses)
            report("OK" if abs(m - 3.05) < 0.35 else "FALHA",
                   f"perda média em {len(losses)} fragmentos: {m:.3f} (treino: ≈ 3,05; amostra pequena, variação esperada)")
        t0 = time.time()
        x = torch.randint(0, len(tokenizer), (32, 1023), device=device)
        model.hidden_states(x, layers=[2, 4, 6])
        if device == "cuda":
            torch.cuda.synchronize()
        dt = time.time() - t0
        report("OK", f"extração: {32 / dt:.0f} fragmentos/s → ~{50177 / (32 / dt) / 60:.1f} min para o acervo")
        t0 = time.time()
        generate(model, list(range(1, 513)), max_new_tokens=32)
        per_tok = (time.time() - t0) / 32
        report("OK", f"geração: {per_tok * 1000:.0f} ms/token → ~{per_tok * 256:.0f} s por continuação de 256 tokens")
else:
    report("FALHA", "checkpoint não informado ou inexistente (--checkpoint ou CV_CHECKPOINT)")

print("\nResumo:", "tudo pronto" if not problems else f"{len(problems)} falha(s):")
for p in problems:
    print("  -", p)
