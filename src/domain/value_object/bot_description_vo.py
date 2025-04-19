from pydantic import BaseModel


class BotDescriptionVO(BaseModel):
    value: str
