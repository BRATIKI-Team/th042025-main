from dataclasses import dataclass

from src.domain.enum.source_status_enum import SourceStatus


@dataclass
class SourceModel:
    id: int
    name: str
    status: SourceStatus
    url: str
    description: str
