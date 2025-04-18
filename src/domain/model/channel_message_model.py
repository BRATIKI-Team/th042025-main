from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from src.domain.model.channel_attachment_model import ChannelAttachmentModel


class ChannelMessageModel(BaseModel):
    """Model for Telegram messages"""

    message_id: int = Field(..., description="Message ID")
    date: datetime = Field(..., description="Message date")
    text: str = Field("", description="Message text")
    attachments: List[ChannelAttachmentModel] = Field(
        default_factory=list, description="Message attachments"
    )
    source: Optional[str] = Field(None, description="Source channel ID")
