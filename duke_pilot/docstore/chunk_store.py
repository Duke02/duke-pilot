from duke_pilot.docstore.docstore import get_docs, add_docs, query_docs


def add_chunks(chunks: list[str]):
    return add_docs(chunks, 'chunks')


def get_chunks(chunk_ids: list[str]) -> list[str]:
    """
    Gets specific chunks from the doc-store by the provided chunk_ids.
    :param chunk_ids: The specific IDs of chunks to get.
    :return: The text of the chunks.
    """
    return get_docs(chunk_ids, 'chunks')


def query_chunks(query_text: str, limit: int = 10) -> list[tuple[str, str]]:
    """
    Queries the chunk store by the provided query_text.
    :param query_text: The text to query the chunk collection within the doc-store for.
    :param limit: The max number of chunks to get.
    :return: A list of tuples in the format of [(chunk id, chunk text), ...]
    """
    return query_docs(query_text, collection_name='chunks', limit=limit)