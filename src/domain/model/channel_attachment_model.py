from typing import Optional
from pydantic import BaseModel, Field


class ChannelAttachmentModel(BaseModel):
    """Model for message attachments"""

    channel_username: str = Field(..., description="channel name")
    message_id: int = Field(..., description="message id")
    type: str = Field(..., description="Type of attachment (photo, document, etc.)")
    file_id: str = Field(..., description="File ID")
    file_name: Optional[str] = Field(None, description="File name for documents")
    mime_type: Optional[str] = Field(None, description="MIME type of the file")
    size: Optional[int] = Field(None, description="File size in bytes")
