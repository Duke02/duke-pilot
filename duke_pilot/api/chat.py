from fastapi import APIRouter
from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult

from duke_pilot.api.models.chat import ChatCompletionRequest, ChatCompletionResponse, ChatMessage
from duke_pilot.prompter.prompter import get_agent
from duke_pilot.utils.model_utils import convert_to_role_content

router: APIRouter = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/completions')
async def chat_completions(request: ChatCompletionRequest) -> ChatCompletionResponse:
    # https://towardsdatascience.com/how-to-build-an-openai-compatible-api-87c8edea2f06/
    agent: Agent = get_agent()
    run_out: AgentRunResult = await agent.run(user_prompt=request.user_prompt, message_history=request.message_history)
    return ChatCompletionResponse(object='chat.completion', model=agent.model.model_name,
                                  choices=[ChatMessage(role=cm['assistant'], content=cm['content']) for m in
                                           run_out.new_messages() if
                                           (cm := convert_to_role_content(m))['role'] == 'assistant' and cm[
                                               'kind'] == 'text'])



