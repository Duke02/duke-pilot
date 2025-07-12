import os
import typing as tp

import numpy as np
import qdrant_client
from qdrant_client.models import *

from duke_pilot.utils.path_helper import get_data_directory
from duke_pilot.processors.embedder import get_embedder, Embedder
from duke_pilot.utils.uuid import get_uuid


# communicate with our Docker compose doc-store container
client: qdrant_client.QdrantClient = qdrant_client.QdrantClient(url=f'http://doc-store:{os.getenv("QDRANT_PORT")}')
embedder: Embedder = get_embedder()


def add_chunk(chunk_text: list[str]):
    ids: list[str] = [get_uuid() for _ in range(len(chunk_text))]
    if not client.collection_exists('chunks'):
        client.create_collection('chunks')
    embedding: np.ndarray = embedder.encode(chunk_text)
    client.upsert(collection_name='chunks',
                  points=[PointStruct(id=chunk_id, vector=e, payload={'text': chunk}) for chunk_id, e, chunk in
                          zip(ids, embedding, chunk_text)])


def get_chunks(chunk_ids: list[str]) -> list[str]:
    records: list[Record] = client.retrieve(collection_name='chunks', ids=chunk_ids)
    return [rec.payload['text'] for rec in records]


def query_chunks(query_text: str, limit: int = 10) -> list[str]:
    embedding: np.ndarray = embedder.encode([query_text])
    resp: QueryResponse = client.query_points(collection_name='chunks', points=embedding[0], limit=limit, with_payload=True)
    return [p.payload['text'] for p in resp.points]

