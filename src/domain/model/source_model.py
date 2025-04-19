from dataclasses import dataclass
from datetime import datetime

from src.domain.enum.source_status_enum import SourceStatus
from src.domain.enum.source_type_enum import SourceType


@dataclass
class SourceModel:
    id: int
    name: str
    status: SourceStatus
    url: str
    description: str
    type: SourceType
    last_hit_datetime: datetime | None = None
