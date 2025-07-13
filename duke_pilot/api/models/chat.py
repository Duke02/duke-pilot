import datetime

from pydantic import BaseModel, Field

from duke_pilot.utils.uuid import get_uuid


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = 'Qwen/Qwen3-4B-FP8'
    messages: list[ChatMessage]
    max_tokens: int | None = 512
    temperature: float | None = 0.1
    stream: bool | None = False


class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: get_uuid())
    object: str
    created: datetime.time = Field(default_factory=lambda: datetime.datetime.now().time())
    model: str
    choices: list[ChatMessage]
