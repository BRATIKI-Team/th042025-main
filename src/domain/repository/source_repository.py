from abc import ABC, abstractmethod
from typing import List

from src.domain.enum.source_status_enum import SourceStatus
from src.domain.model.pagination_model import PaginationModel
from src.domain.model.source_model import SourceModel


class SourceRepository(ABC):
    @abstractmethod
    async def get_source_by_status(
        self, bot_id: int, status: SourceStatus
    ) -> SourceModel | None:
        pass

    @abstractmethod
    async def update_last_hit_datetime(self, source_ids: List[int]) -> None:
        """
        Update the last_hit_datetime for the given source IDs to the current time.
        """

    @abstractmethod
    async def validate_topic(self, topic: str) -> bool:
        pass

    @abstractmethod
    async def search_sources(self, bot_id: int, topic: str) -> None:
        pass

    @abstractmethod
    async def change_status(self, id: int, status: SourceStatus) -> None:
        pass

    @abstractmethod
    async def has_rejected_source(self, bot_id: int) -> bool:
        pass

    @abstractmethod
    async def has_accepted_source(self, bot_id: int) -> bool:
        pass

    @abstractmethod
    async def get_bot_sources(
        self, bot_id: int, status: SourceStatus, page: int, page_size: int
    ) -> PaginationModel[SourceModel]:
        pass

    @abstractmethod
    async def get_by_bot_id(self, bot_id: int) -> List[SourceModel]:
        pass
