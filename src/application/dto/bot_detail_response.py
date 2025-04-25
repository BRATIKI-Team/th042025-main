from datetime import datetime

from pydantic import BaseModel

from src.application.dto.source_response import SourceResponse
from src.domain.enum.bot_status_enum import BotStatus


class BotDetailResponse(BaseModel):
    id: int
    name: str
    topic: str
    status: BotStatus
    users_count: int
    sources: list[SourceResponse]
    metrics: dict[str, int]
