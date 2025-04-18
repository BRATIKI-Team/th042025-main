from abc import ABC, abstractmethod

from src.domain.enum.source_status_enum import SourceStatus
from src.domain.model.source_model import SourceModel


class SourceRepository(ABC):
    @abstractmethod
    async def get_source_by_status(self, status: SourceStatus) -> SourceModel | None:
        pass
