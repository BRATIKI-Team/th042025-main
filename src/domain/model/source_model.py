from dataclasses import dataclass
from datetime import datetime

from src.domain.enum.source_status_enum import SourceStatus


@dataclass
class SourceModel:
    id: int
    name: str
    status: SourceStatus
    url: str
    description: str
    type: int
    last_hit_datetime: datetime | None = None
