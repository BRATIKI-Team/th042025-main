from pydantic import BaseModel, field_validator


class BotTokenVO(BaseModel):
    value: str

    @field_validator("value")
    def validate_token(cls, v: str) -> str:
        if len(v) != 46:
            raise ValueError("Invalid bot token")
        return v
