"""Music Transformer usado no treino (cópia fiel da arquitetura do notebook
`referencia/Composer_Vector_GiantModel.ipynb`), com utilitários de extração
e geração com steering.

Regras: este módulo é somente-leitura para as frentes F2–F7. Mudanças aqui
passam pela F0, porque alteram todas as representações.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

# Hiperparâmetros do checkpoint_epoch_93.pt (GiantMIDI, surname_checked)
D_MODEL, N_HEADS, N_LAYERS, FF_DIM, DROPOUT = 512, 8, 6, 2048, 0.1
MAX_SEQ_LEN = 1024


def precompute_freqs_cis(dim: int, end: int, theta: float = 10000.0):
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim))
    t = torch.arange(end, device=freqs.device, dtype=torch.float32)
    freqs = torch.outer(t, freqs).float()
    return torch.polar(torch.ones_like(freqs), freqs)


def apply_rope(xq, xk, freqs_cis):
    xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))
    freqs_cis = freqs_cis.view(1, 1, freqs_cis.shape[0], freqs_cis.shape[1])
    xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(3)
    xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(3)
    return xq_out.type_as(xq), xk_out.type_as(xk)


class CustomAttentionBlock(nn.Module):
    def __init__(self, d_model, n_heads, dropout):
        super().__init__()
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.qkv = nn.Linear(d_model, d_model * 3, bias=False)
        self.proj = nn.Linear(d_model, d_model, bias=False)
        self.dropout_p = dropout

    def forward(self, x, freqs_cis):
        B, T, C = x.shape
        qkv = self.qkv(x).reshape(B, T, 3, self.n_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]
        q, k = apply_rope(q, k, freqs_cis)
        p = self.dropout_p if self.training else 0.0
        out = F.scaled_dot_product_attention(q, k, v, is_causal=True, dropout_p=p)
        return self.proj(out.transpose(1, 2).reshape(B, T, C))


class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, ff_dim, dropout):
        super().__init__()
        self.attn = CustomAttentionBlock(d_model, n_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(nn.Linear(d_model, ff_dim), nn.GELU(), nn.Dropout(dropout), nn.Linear(ff_dim, d_model))
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, freqs_cis):
        x = x + self.dropout(self.attn(self.norm1(x), freqs_cis))
        x = x + self.dropout(self.ff(self.norm2(x)))
        return x


class MusicTransformer(nn.Module):
    def __init__(self, vocab_size, d_model=D_MODEL, max_seq_len=MAX_SEQ_LEN, n_heads=N_HEADS,
                 n_layers=N_LAYERS, ff_dim=FF_DIM, dropout=DROPOUT):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.register_buffer("freqs_cis", precompute_freqs_cis(d_model // n_heads, max_seq_len * 2))
        self.layers = nn.ModuleList([TransformerBlock(d_model, n_heads, ff_dim, dropout) for _ in range(n_layers)])
        self.final_norm = nn.LayerNorm(d_model)
        self.output_head = nn.Linear(d_model, vocab_size, bias=False)
        self.token_embedding.weight = self.output_head.weight
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, steering_vector=None, steering_layer=-1, alpha=1.0):
        """Igual ao treino. Steering: h <- (h + a v) * |h| / |h + a v| na camada alvo, em todas as posições."""
        T = x.shape[1]
        h = self.dropout(self.token_embedding(x))
        freqs_cis = self.freqs_cis[:T]
        target = len(self.layers) - 1 if steering_layer == -1 else steering_layer
        for idx, layer in enumerate(self.layers):
            h = layer(h, freqs_cis)
            if steering_vector is not None and idx == target:
                s = steering_vector.view(1, 1, -1).to(h.dtype)
                n0 = torch.linalg.vector_norm(h, dim=-1, keepdim=True)
                hs = h + alpha * s
                h = hs * (n0 / (torch.linalg.vector_norm(hs, dim=-1, keepdim=True) + 1e-8))
        return self.output_head(self.final_norm(h))

    @torch.no_grad()
    def hidden_states(self, x, layers=None):
        """Estados ocultos por camada. Índice 0 = embedding de entrada; 1..N = saída do bloco i
        (antes da norma final, como no repo original). Retorna dict camada -> (last_token, mean_pool)."""
        self.eval()
        layers = set(range(len(self.layers) + 1)) if layers is None else set(layers)
        T = x.shape[1]
        h = self.token_embedding(x)
        out = {}
        if 0 in layers:
            out[0] = (h[:, -1, :], h.mean(dim=1))
        freqs_cis = self.freqs_cis[:T]
        for idx, layer in enumerate(self.layers, start=1):
            h = layer(h, freqs_cis)
            if idx in layers:
                out[idx] = (h[:, -1, :], h.mean(dim=1))
        return out


def load_model(checkpoint_path, vocab_size, device="cpu"):
    model = MusicTransformer(vocab_size).to(device)
    ckpt = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    return model, ckpt


@torch.no_grad()
def generate(model, seed_tokens, steering_vector=None, alpha=0.0, steering_layer=-1, max_new_tokens=256,
             temperature=0.95, top_k=40, top_p=1.0, repetition_penalty=1.5, generator=None):
    """Mesma amostragem do notebook (top-k, top-p, penalidade de repetição nos últimos 30 tokens).
    `steering_layer` segue a convenção do forward: índice 0-based do bloco, -1 = último."""
    model.eval()
    device = next(model.parameters()).device
    generated = list(seed_tokens)
    for _ in range(max_new_tokens):
        x = torch.tensor([generated[-(MAX_SEQ_LEN - 1):]], dtype=torch.long, device=device)
        logits = model(x, steering_vector=steering_vector, steering_layer=steering_layer, alpha=alpha)[0, -1].float()
        for tok in set(generated[-30:]):
            logits[tok] = logits[tok] / repetition_penalty if logits[tok] > 0 else logits[tok] * repetition_penalty
        logits = logits / temperature
        if top_k > 0:
            v, ind = torch.topk(logits, min(top_k, logits.size(-1)))
            logits = torch.full_like(logits, float("-inf"))
            logits[ind] = v
        probs = torch.softmax(logits, dim=-1)
        sp, si = torch.sort(probs, descending=True)
        remove = torch.cumsum(sp, dim=-1) > top_p
        remove[1:] = remove[:-1].clone()
        remove[0] = False
        probs[si[remove]] = 0.0
        probs = probs / probs.sum()
        generated.append(torch.multinomial(probs, 1, generator=generator).item())
    return generated
