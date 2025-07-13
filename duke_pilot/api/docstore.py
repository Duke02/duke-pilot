import logging
import typing as tp

from fastapi import APIRouter, status, UploadFile, Response
from fastapi.responses import JSONResponse

from duke_pilot.api.models.docstore import Chunk, Memory, QueryResponse, QueryRequest, QueryResponseItem, IngestResponse
from duke_pilot.api.models.parser import ParseResponse
from duke_pilot.api.parser import parse
from duke_pilot.docstore.chunk_store import get_chunks, add_chunks, query_chunks
from duke_pilot.docstore.memory_store import get_memories, query_memories
from duke_pilot.processors.chunker import Chunker
from duke_pilot.processors.embedder import Embedder, get_embedder
from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)

router: APIRouter = APIRouter(prefix='/docstore', tags=['docstore'])

@router.get('/chunks/{chunk_id}')
async def get_chunk(chunk_id: str) -> Chunk:
    chunk_text: str = get_chunks([chunk_id])[0]
    return Chunk(chunk_id=chunk_id, chunk_text=chunk_text)


@router.put('/ingest')
async def ingest(file: UploadFile, force_parse: bool = False, chunk_similarity_threshold: float = 0.5) -> IngestResponse:
    logger.info(f'Ingesting file with file {file.filename}')
    parse_resp: ParseResponse = await parse(file, force=force_parse)
    if not parse_resp.successful:
        logger.error('Parsing failed!')
        return IngestResponse(parse_response=parse_resp, chunks=None)
    logger.debug('Parsing was successful!')
    embedder: Embedder = get_embedder()
    chunker: Chunker = Chunker(embedder=embedder, similarity_threshold=chunk_similarity_threshold)
    chunk_texts: list[str] = chunker.chunk(parse_resp.text)
    chunk_ids: list[str] = add_chunks(chunk_texts)
    chunks: list[Chunk] = [Chunk(chunk_id=cid, chunk_text=ctext) for cid, ctext in zip(chunk_ids, chunk_texts)]
    return IngestResponse(parse_response=parse_resp, chunks=chunks)


@router.get('/memories/{memory_id}')
async def get_memory(memory_id: str) -> Memory:
    memory_text: str = get_memories([memory_id])[0]
    return Memory(memory_id=memory_id, memory=memory_text)


@router.post('/query', status_code=status.HTTP_200_OK)
async def query(request: QueryRequest, response: Response = Response()) -> QueryResponse:
    logger.debug(f'Got query request', query_request=request)
    if request.to_query == 'chunk':
        chunk_text: list[tuple[str, str]] = query_chunks(request.query, limit=request.limit)
        chunks: list[Chunk] = [Chunk(chunk_id=cid, chunk_text=ctext) for cid, ctext in chunk_text]
        return QueryResponse(items=[QueryResponseItem(object=c) for c in chunks], query=request.query)
    elif request.to_query == 'memory':
        memories: list[tuple[str, str]] = query_memories(request.query, limit=request.limit)
        mems: list[Memory] = [Memory(memory_id=mid, memory=mem) for mid, mem in memories]
        return QueryResponse(items=[QueryResponseItem(object=m) for m in mems], query=request.query)
    else:
        logger.error(f'Incorrect to_query field ({request.to_query=})')
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return QueryResponse(items=[], query=request.query)

