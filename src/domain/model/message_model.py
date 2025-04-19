from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class MessageModel(BaseModel):
    id: Optional[int] = Field(None, description="The unique identifier of the message")
    source_id: int = Field(
        ..., description="The identifier for the source of the message"
    )
    content: str = Field(..., description="The text content of the message")
    external_id: str = Field(
        ..., description="External identifier associated with the message"
    )
    created_at: datetime = Field(
        ..., description="The timestamp when the message was created"
    )
    published_at: Optional[datetime] = Field(
        None, description="The timestamp when the message was published (if applicable)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the message (e.g., timestamp, author, etc.)",
    )
