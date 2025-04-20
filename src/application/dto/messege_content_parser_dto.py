from typing import Optional
from pydantic import BaseModel, Field


class MessageContentParserDto(BaseModel):
    id: Optional[int] = Field(None, description="The unique identifier of the message")
    content: str = Field(..., description="The text content of the message")