from pydantic import BaseModel

from src.domain.enum.bot_status_enum import BotStatus


class BotLightResponse(BaseModel):
    id: int
    name: str
    topic: str
    status: BotStatus
