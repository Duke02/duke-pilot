from pydantic import BaseModel


class ParseResponse(BaseModel):
    successful: bool
    text: str | None
    file_ext_used: str
    error: str | None = None
