import os
import typing as tp

import numpy as np
import qdrant_client
# from qdrant_client.models import
from qdrant_client.models import PointStruct, Record, QueryResponse, ScoredPoint

from duke_pilot.utils.path_helper import get_data_directory
from duke_pilot.processors.embedder import get_embedder, Embedder
from duke_pilot.utils.uuid import get_uuid


# communicate with our Docker compose doc-store container
client: qdrant_client.QdrantClient = qdrant_client.QdrantClient(url=f'http://doc-store:{os.getenv("QDRANT_PORT")}')
embedder: Embedder = get_embedder()


def add_docs(texts: list[str], collection_name: str) -> list[str]:
    ids: list[str] = [get_uuid() for _ in range(len(texts))]
    if not client.collection_exists(collection_name):
        client.create_collection(collection_name)
    embedding: np.ndarray = embedder.encode(texts)
    client.upsert(collection_name=collection_name,
                  points=[PointStruct(id=text_id, vector=e, payload={'text': txt}) for text_id, e, txt in
                          zip(ids, embedding, texts)])
    return ids


def get_docs(ids: list[str], collection_name: str) -> list[str]:
    records: list[Record] = client.retrieve(collection_name=collection_name, ids=ids)
    return [rec.payload['text'] for rec in records]


def query_docs(query_text: str, collection_name: str, limit: int = 10) -> list[tuple[str, str]]:
    embedding: np.ndarray = embedder.encode([query_text])
    points: list[ScoredPoint] = client.query_points(collection_name=collection_name, points=embedding[0], limit=limit, with_payload=True).points
    return [(p.id, p.payload['text']) for p in points]

