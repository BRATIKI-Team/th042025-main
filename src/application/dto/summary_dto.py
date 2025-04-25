from typing import Optional
from pydantic import BaseModel, Field


class SummaryDto(BaseModel):
    """Represents a summary with the title, content, and metadata."""

    title: str = Field(
        ...,
        description="Title of the summary",
        example="Rosneft announced dividend payment",
    )
    content: str = Field(
        ..., description="Main content of the summary, providing a concise overview"
    )
    metadata: dict = Field(
        ...,
        description="Additional metadata related to the summary, such as the source",
        example={"source": "https://www.google.com"},
    )


class SummaryExtendedDto(SummaryDto):
    image_url: Optional[str] = Field(
        default=None, description="URL of the image associated with the summary"
    )
