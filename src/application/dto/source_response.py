from pydantic import BaseModel

from src.domain.enum.source_type_enum import SourceType


class SourceResponse(BaseModel):
    id: int
    name: str
    description: str
    type: SourceType
    url: str
