from typing import Any

from fastapi.responses import Response
from pydantic import BaseModel


class ParseResponse(BaseModel):
    successful: bool
    text: str | None
    file_ext_used: str
    error: str | None = None


# class ParseResponse(Response, BaseModel):
#     media_type: str = 'application/json'
#
#     def render(self, content: Any) -> bytes | memoryview:
#         if isinstance(content, ParseResponseContent):
#             return content.model_dump_json().encode(self.charset)
#         else:
#             return str(content).encode(self.charset)
#
