from pydantic_ai import Agent, Tool

from duke_pilot.docstore.chunk_store import get_chunks, query_chunks
from duke_pilot.docstore.memory_store import get_memories, add_memories, query_memories
from duke_pilot.prompter.model import HuggingFaceLocalModel


def get_agent() -> Agent:
    if hasattr(get_agent, 'agent'):
        return getattr(get_agent, 'agent')
    model: HuggingFaceLocalModel = HuggingFaceLocalModel()
    agent: Agent = Agent(model=model, tools=[
        Tool(get_chunks, takes_ctx=False),
        Tool(query_chunks, takes_ctx=False),
        Tool(get_memories, takes_ctx=False),
        Tool(add_memories, takes_ctx=False),
        Tool(query_memories, takes_ctx=False),
    ])
    setattr(get_agent, 'agent', agent)
    return agent
