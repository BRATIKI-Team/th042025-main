from pydantic import BaseModel, field_validator


class BotNameVO(BaseModel):
    value: str

    @field_validator("value")
    def validate_name(cls, v: str) -> str:
        if len(v) > 255:
            raise ValueError("Name must be less than 255 characters")
        return v
