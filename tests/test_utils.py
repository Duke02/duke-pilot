from pathlib import Path

from mistralai import ToolCall
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart, SystemPromptPart, ToolReturn, \
    ToolReturnPart, RetryPromptPart, ModelResponse, TextPart, ToolCallPart, ThinkingPart

from duke_pilot.utils.path_helper import get_base_directory, get_logs_directory, get_data_directory, get_model_directory
from duke_pilot.utils.uuid import get_uuid
from duke_pilot.utils.model_utils import convert_to_role_content

def test_path_helpers():
    true_base_dir: Path = Path(__file__).resolve().parent.parent
    assert true_base_dir == get_base_directory()

    assert get_logs_directory() == true_base_dir / 'logs'
    assert get_data_directory() == true_base_dir / 'data'
    assert get_model_directory() == true_base_dir / 'models'


def test_uuid_helper():
    u: str = get_uuid()
    assert isinstance(u, str)
    assert len(u) > 0


def test_convert_from_user_prompt():
    req: ModelRequest = ModelRequest(parts=[UserPromptPart(content='This is a test message')])
    d: dict[str, str] = convert_to_role_content(req)
    assert d['content'] == 'This is a test message'
    assert d['role'] == 'user'
    assert d['kind'] == 'user'


def test_convert_from_system_prompt():
    req: ModelRequest = ModelRequest(parts=[SystemPromptPart(content='This is a test message')])
    d: dict[str, str] = convert_to_role_content(req)
    assert d['content'] == 'This is a test message'
    assert d['role'] == 'user'
    assert d['kind'] == 'system'


def test_convert_from_tool_return():
    req: ModelRequest = ModelRequest(
        parts=[ToolReturnPart(content='This is a test message', tool_name='Test Tool', tool_call_id=get_uuid())])
    d: dict[str, str] = convert_to_role_content(req)
    assert d['content'] == 'This is a test message'
    assert d['role'] == 'user'
    assert d['kind'] == 'tool'


def test_convert_from_retry_prompt():
    req: ModelRequest = ModelRequest(parts=[RetryPromptPart(content='This is a test message')])
    d: dict[str, str] = convert_to_role_content(req)
    assert d['content'] == 'This is a test message'
    assert d['role'] == 'user'
    assert d['kind'] == 'retry'


def test_convert_from_text():
    resp: ModelResponse = ModelResponse(parts=[TextPart(content='This is a test message')])
    d: dict[str, str] = convert_to_role_content(resp)
    assert d['content'] == 'This is a test message'
    assert d['role'] == 'assistant'
    assert d['kind'] == 'text'


def test_convert_from_tool_call():
    tool_call_id: str = get_uuid()
    resp: ModelResponse = ModelResponse(parts=[ToolCallPart(tool_name='Test Tool', tool_call_id=tool_call_id)])
    d: dict[str, str] = convert_to_role_content(resp)
    assert d['content'] == f'Tool "Test Tool" (Call-ID: {tool_call_id}) called with args: {{}}'
    assert d['role'] == 'assistant'
    assert d['kind'] == 'tool'




def test_convert_from_thinking():
    resp: ModelResponse = ModelResponse(parts=[ThinkingPart(content='This is a test message')])
    d: dict[str, str] = convert_to_role_content(resp)
    assert d['content'] == 'This is a test message'
    assert d['role'] == 'assistant'
    assert d['kind'] == 'think'


