import logging
import typing as tp

from pydantic_ai.messages import ModelMessage, ModelResponse, ModelRequest, ToolCallPart, TextPart, ThinkingPart, \
    ModelRequestPart, ToolReturnPart, UserPromptPart, SystemPromptPart, RetryPromptPart

from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)


@logger.log
def convert_to_role_content(msg: ModelMessage) -> dict[str, str]:
    msg: ModelRequest | ModelResponse
    if isinstance(msg, ModelRequest):
        part: ModelRequestPart = msg.parts[-1]
        kind: str = ''
        if isinstance(part, ToolReturnPart):
            kind: str = 'tool'
        elif isinstance(part, UserPromptPart):
            kind: str = 'user'
        elif isinstance(part, SystemPromptPart):
            kind: str = 'system'
        elif isinstance(part, RetryPromptPart):
            kind: str = 'retry'
        role: str = 'user'
        content: str = part.content
        return dict(role=role, content=content, kind=kind)
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
