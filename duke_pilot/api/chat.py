from fastapi import APIRouter
from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult

from duke_pilot.api.models.chat import ChatCompletionRequest, ChatCompletionResponse, ChatMessage
from duke_pilot.prompter.prompter import get_agent
from duke_pilot.utils.model_utils import convert_to_role_content
from duke_pilot.utils.log_utils import DukeLogger


router: APIRouter = APIRouter(prefix='/chat', tags=['chat'])
logger: DukeLogger = DukeLogger(__name__)


@router.post('/completions')
async def chat_completions(request: ChatCompletionRequest) -> ChatCompletionResponse:
    # https://towardsdatascience.com/how-to-build-an-openai-compatible-api-87c8edea2f06/
    logger.info(f'Doing chat completions!', chat_request=request)
    agent: Agent = get_agent()
    run_out: AgentRunResult = await agent.run(user_prompt=request.user_prompt, message_history=request.message_history)
    resp: ChatCompletionResponse = ChatCompletionResponse(object='chat.completion', model=agent.model.model_name,
                                  choices=[ChatMessage(role=cm['assistant'], content=cm['content']) for m in
                                           run_out.new_messages() if
                                           (cm := convert_to_role_content(m))['role'] == 'assistant' and cm[
                                               'kind'] == 'text'])
    logger.debug(f'Did chat completions', chat_response=resp)
    return resp
