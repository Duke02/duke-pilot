import enum
import typing as tp
from collections import defaultdict

import accelerate
from nltk import sent_tokenize, word_tokenize
import numpy as np
import transformers

from duke_pilot.processors.embedder import Embedder


class TokenizerOption(enum.Enum):
    Sentence = enum.auto()
    Line = enum.auto()


class Chunker:
    def __init__(self, embedder: Embedder, tokenizer: TokenizerOption = TokenizerOption.Sentence, similarity_threshold: float = 0.5):
        self.embedder: Embedder = embedder
        self.similarity_threshold: float = similarity_threshold
        self.tokenizer: tp.Callable[[str], list[str]] = sent_tokenize if tokenizer is TokenizerOption.Sentence else lambda s: s.splitlines()

    def _allowed(self, similarity_vector: np.ndarray) -> list[int]:
        return np.argwhere(similarity_vector > self.similarity_threshold).tolist()

    def chunk(self, text: str) -> list[str]:
        tokens: list[str] = self.tokenizer(text)
        embeddings: np.ndarray = self.embedder.encode(tokens)
        similarity_matrix: np.ndarray = self.embedder.similarity(embeddings, embeddings)
        chunks: dict[int, str] = {}
        chunks_used: set[int] = set()
        for idx, t in enumerate(tokens):
            if idx in chunks_used:
                continue
            allowed: list[int] = [i for i in self._allowed(similarity_matrix[idx]) if i not in chunks_used]
            chunks_used.update(allowed)
            chunks[idx] = ' '.join([tokens[i] for i in allowed])
        return list(chunks.values())
