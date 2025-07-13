import accelerate
import torch
from pydantic_ai.messages import ModelMessage, ModelResponse, ModelRequest, ToolCallPart, TextPart, ThinkingPart


def convert_to_role_content(msg: ModelMessage) -> dict[str, str]:
    msg: ModelRequest | ModelResponse
    if isinstance(msg, ModelRequest):
        role: str = 'user'
        content: str = msg.parts[-1].content
        return dict(role=role, content=content, kind=msg.kind)
    else:
        msg: ModelResponse
        role: str = 'assistant'
        care_about: TextPart | ToolCallPart | ThinkingPart = msg.parts[-1]
        content: str = ''
        kind: str = ''
        if isinstance(care_about, TextPart):
            content: str = care_about.content
            kind: str = 'text'
        elif isinstance(care_about, ToolCallPart):
            content: str = f'Tool "{care_about.tool_name}" (Call-ID: {care_about.tool_call_id}) called with args: {care_about.args_as_json_str()}'
            kind: str = 'tool'
        elif isinstance(care_about, ThinkingPart):
            content: str = care_about.content
            kind: str = 'think'
        return dict(role=role, content=content, kind=kind)
