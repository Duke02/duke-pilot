import logging
import typing as tp

from duke_pilot.docstore.docstore import get_docs, add_docs, query_docs
from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)


@logger.log
def add_memories(memories: list[str]):
    """
    Adds the provided memories to the docstore. Useful for remembering information about interactions you've had with users.
    :param memories: The memories to save.
    :return: The IDs for the memories you just added to the doc-store.
    """
    return add_docs(memories, 'memories')


@logger.log
def get_memories(memory_ids: list[str]) -> list[str]:
    """
    Gets the specific memories from the docstore.
    :param memory_ids: The specific IDs for the memories you want to get.
    :return: The text of the memories.
    """
    return get_docs(memory_ids, 'memories')


@logger.log
def query_memories(query_text: str, limit: int = 10) -> list[tuple[str, str]]:
    """
    Queries the memory collection from the docstore with the provided text.
    :param query_text: The text to use for your query.
    :param limit: The max number of memories to return.
    :return: A list of tuples in the format of [(memory id, memory text), ...]
    """
    return query_docs(query_text, collection_name='memories', limit=limit)
