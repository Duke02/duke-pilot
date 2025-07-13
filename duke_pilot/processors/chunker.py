import enum
import logging
import typing as tp

from nltk import sent_tokenize
import numpy as np

from duke_pilot.processors.embedder import Embedder
from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)


class TokenizerOption(enum.Enum):
    Sentence = enum.auto()
    Line = enum.auto()


class Chunker:
    @logger.log
    def __init__(self, embedder: Embedder, tokenizer: TokenizerOption = TokenizerOption.Sentence, similarity_threshold: float = 0.5):
        logger.debug(f'Creating a Chunker...', embedder=embedder, tokenizer=tokenizer, similarity_threshold=similarity_threshold)
        self.embedder: Embedder = embedder
        self.similarity_threshold: float = 100 * similarity_threshold
        self.tokenizer: tp.Callable[[str], list[str]] = sent_tokenize if tokenizer is TokenizerOption.Sentence else lambda s: s.splitlines()

    @logger.log
    def _allowed(self, similarity_vector: np.ndarray) -> list[int]:
        sim_val: float = np.percentile(similarity_vector, self.similarity_threshold).item()
        return np.argwhere(similarity_vector > sim_val).reshape(-1).tolist()

    @logger.log
    def chunk(self, text: str) -> list[str]:
        tokens: list[str] = self.tokenizer(text)
        embeddings: np.ndarray = self.embedder.encode(tokens)
        similarity_matrix: np.ndarray = self.embedder.similarity(embeddings, embeddings)
        logger.debug(f'Got similarity matrix', similarity_matrix=similarity_matrix)
        chunks: dict[int, str] = {}
        chunks_used: set[int] = set()
        for idx, t in enumerate(tokens):
            if idx in chunks_used:
                continue
            allowed: list[int] = [i for i in self._allowed(similarity_matrix[idx].reshape(-1)) if i not in chunks_used]
            chunks_used.update(allowed)
            chunks[idx] = ' '.join([tokens[i] for i in allowed])
        return list(chunks.values())

    def __str__(self) -> str:
        return f'Chunker(embedder={self.embedder}, tokenizer={self.tokenizer}, similarity_threshold={self.similarity_threshold})'
