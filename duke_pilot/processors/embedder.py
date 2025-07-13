import functools
import logging
import typing as tp

import accelerate
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
import transformers

from duke_pilot.utils.path_helper import get_model_directory
from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)


class Embedder:
    @logger.log
    def __init__(self, model_name: str = 'Qwen/Qwen3-Embedding-0.6B'):
        logger.debug(f'Creating embedder using model {model_name}')
        self.model_name: str = model_name
        self.model: SentenceTransformer = SentenceTransformer(self.model_name, cache_folder=str(get_model_directory()),
                                                              model_kwargs={'torch_dtype': torch.float16})

    def __str__(self) -> str:
        return f'Embedder(model={self.model_name}, embedding_size={self.embedding_size})'

    @functools.cached_property
    def embedding_size(self) -> int:
        return self.encode(['A']).shape[1]

    @logger.log
    def encode(self, text: list[str]) -> np.ndarray:
        """
        Encodes the embedding of the provided texts.
        :param text: The texts to find the embedding of.
        :return: A matrix of the embeddings in the shape of [N_text, EMBEDDING_SIZE]
        """
        return self.model.encode(text)

    @logger.log
    def similarity(self, text1: list[str] | np.ndarray, text2: list[str] | np.ndarray) -> torch.Tensor:
        """
        Calculates the similarity between text1 and text2.
        :param text1: The first text.
        :param text2: The second text.
        :return: A Tensor in the shape of N_text1 x N_text2.
        """
        return self.model.similarity(text1, text2)


@logger.log
def get_embedder() -> Embedder:
    already_made_an_embedder: bool = hasattr(get_embedder, 'embedder')
    logger.debug(f'Requesting an Embedder. Already created one? {already_made_an_embedder}')
    if already_made_an_embedder:
        return getattr(get_embedder, 'embedder')
    setattr(get_embedder, 'embedder', Embedder())
    return getattr(get_embedder, 'embedder')
