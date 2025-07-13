from typing import Literal

from pydantic import BaseModel, Field

from duke_pilot.api.models.parser import ParseResponse


class Chunk(BaseModel):
    kind: str = 'chunk'
    chunk_id: str
    chunk_text: str


class Memory(BaseModel):
    kind: str = 'memory'
    memory_id: str
    memory: str


class QueryRequest(BaseModel):
    query: str
    to_query: Literal['chunk'] | Literal['memory']
    limit: int = 10


class QueryResponseItem(BaseModel):
    object: Chunk | Memory = Field(discriminator='kind')


class QueryResponse(BaseModel):
    items: list[QueryResponseItem]
    query: str


class IngestResponse(BaseModel):
    parse_response: ParseResponse
    chunks: list[Chunk] | None