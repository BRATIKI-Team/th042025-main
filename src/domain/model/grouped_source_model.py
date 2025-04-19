from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel


class SourceInfo(BaseModel):
    id: int
    bot_id: int
    bot_notification_period: int
    bot_last_notified_at: Optional[datetime] = None


class GroupedSourceModel(BaseModel):
    url: str
    type: int
    sources: List[SourceInfo]
    last_hit_datetime: datetime
    notification_period: int 