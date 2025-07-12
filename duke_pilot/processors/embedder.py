import functools

import accelerate
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
import transformers

from duke_pilot.utils.path_helper import get_model_directory


class Embedder:
    def __init__(self, model_name: str = 'Qwen/Qwen3-Embedding-0.6B'):
        self.model_name: str = model_name
        self.model: SentenceTransformer = SentenceTransformer(self.model_name, cache_folder=str(get_model_directory()),
                                                              model_kwargs={'torch_dtype': torch.float16})

    @functools.cached_property
    def embedding_size(self) -> int:
        return self.encode(['A']).shape[1]

    def encode(self, text: list[str]) -> np.ndarray:
        """
        Encodes the embedding of the provided texts.
        :param text: The texts to find the embedding of.
        :return: A matrix of the embeddings in the shape of [N_text, EMBEDDING_SIZE]
        """
        return self.model.encode(text)

    def similarity(self, text1: list[str] | np.ndarray, text2: list[str] | np.ndarray) -> torch.Tensor:
        """
        Calculates the similarity between text1 and text2.
        :param text1: The first text.
        :param text2: The second text.
        :return: A Tensor in the shape of N_text1 x N_text2.
        """
        return self.model.similarity(text1, text2)


def get_embedder() -> Embedder:
    if hasattr(get_embedder, 'embedder'):
        return getattr(get_embedder, 'embedder')
    setattr(get_embedder, 'embedder', Embedder())
    return getattr(get_embedder, 'embedder')
