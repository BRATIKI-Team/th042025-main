from typing import Optional
from pydantic import BaseModel, Field


class ChannelInfoModel(BaseModel):
    """Model for channel information"""

    id: int = Field(..., description="Channel ID")
    title: str = Field(..., description="Channel title")
    username: Optional[str] = Field(None, description="Channel username")
    description: Optional[str] = Field(None, description="Channel description")
    photo_url: Optional[str] = Field(None, description="Channel photo URL")
    participants_count: Optional[int] = Field(
        None, description="Number of participants"
    )
    is_verified: bool = Field(False, description="Whether the channel is verified")
