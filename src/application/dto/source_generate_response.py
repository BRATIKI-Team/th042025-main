from pydantic import BaseModel, Field, HttpUrl


class SourceGenerateResponse(BaseModel):
    url: str = Field(
        ...,
        description="The URL of the Telegram channel in @channelname format",
        examples=["@python_ru", "@devops_ru"]
    )
    description: str = Field(
        ...,
        description="Brief description of the channel's content and focus area",
        min_length=10,
        max_length=200,
        examples=["Channel where you can find actual news about Python programming and development"]
    )