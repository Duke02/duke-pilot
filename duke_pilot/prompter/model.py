import logging
import typing as tp

from pydantic_ai.messages import ModelMessage, ModelResponse, ModelRequest, SystemPromptPart, UserPromptPart, \
    ToolReturnPart, RetryPromptPart, TextPart, ToolCallPart, ThinkingPart
from pydantic_ai.models import Model, ModelRequestParameters
from pydantic_ai.settings import ModelSettings
import transformers

from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)


class HuggingFaceLocalModel(Model):
    @logger.log
    def __init__(self, model_name: str = 'Qwen/Qwen3-4B-FP8', **kwargs):
        super().__init__()
        logger.debug(f'Creating local HuggingFace model with model {model_name}')
        if not model_name.startswith("Qwen/"):
            raise ValueError("model_name must start with 'Qwen'")
        self._model_name: str = model_name
        self.tokenizer: transformers.AutoTokenizer = transformers.AutoTokenizer.from_pretrained(model_name, **kwargs)
        self.model: transformers.AutoModel = transformers.AutoModel.from_pretrained(model_name, **kwargs)

    def __str__(self) -> str:
        return f'HuggingFaceLocalModel(model_name={self.model_name})'

    @logger.alog
    async def request(self, messages: list[ModelMessage], model_settings: ModelSettings | None,
                      model_request_parameters: ModelRequestParameters) -> ModelResponse:
        logger.debug(f'Requesting response from model {self._model_name}', messages=messages)
        # From: https://huggingface.co/Qwen/Qwen3-4B-FP8#quickstart
        text: str = self.tokenizer.apply_chat_template(
            [HuggingFaceLocalModel._convert_to_role_content(m) for m in messages], tokenize=False,
            add_generation_prompt=True, enable_thinking=True)
        model_inputs = self.tokenizer([text], return_tensors='pt').to(self.model.device)
        generated_ids = self.model.generate(**model_inputs, max_new_tokens=32768)
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
        # parsing thinking content
        try:
            # rindex finding 151668 (</think>)
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0
        thinking_content = self.tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        content = self.tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
        out: ModelResponse = ModelResponse(parts=[ThinkingPart(content=thinking_content), TextPart(content=content)],
                             model_name=self.model_name)
        logger.debug(f'Got response from {self.model_name}', out=out)
        return out

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def system(self) -> str:
        return 'huggingface_local'
