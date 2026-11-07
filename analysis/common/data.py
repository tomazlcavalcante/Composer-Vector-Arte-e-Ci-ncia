"""Leitura do acervo GiantMIDI (surname_checked_midis) com chave de compositor correta.

Nomes de arquivo: "Sobrenome, Nome, Título, youtube_id.mid".
O repo original usava só o sobrenome, fundindo J. S. Bach com C. P. E. Bach,
Robert com Clara Schumann, Cyril com James Scott etc. Aqui a chave é "Sobrenome, Nome".
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Piece:
    path: Path
    surname: str
    firstname: str
    title: str
    youtube_id: str

    @property
    def composer_key(self) -> str:
        return f"{self.surname}, {self.firstname}"

    @property
    def piece_id(self) -> str:
        return self.path.stem


def parse_name(path: Path) -> Piece:
    parts = [p.strip() for p in path.stem.split(",")]
    surname, firstname = parts[0], parts[1] if len(parts) > 1 else ""
    youtube_id = parts[-1] if len(parts) > 3 else ""
    title = ", ".join(parts[2:-1]) if len(parts) > 3 else ", ".join(parts[2:])
    return Piece(path, surname, firstname, title, youtube_id)


def list_pieces(dataset_dir: str | Path) -> list[Piece]:
    """Ordem determinística (o glob do repo original dependia do sistema de arquivos)."""
    return [parse_name(p) for p in sorted(Path(dataset_dir).glob("*.mid"))]


def fragments(token_ids: list[int], length: int = 1024, stride: int = 1024):
    """Mesmo fatiamento do treino: janelas sem sobreposição; o resto final é descartado."""
    for i in range(0, len(token_ids) - length, stride):
        yield i // stride, token_ids[i : i + length]
