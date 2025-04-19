from typing import List

from src.domain.model.grouped_source_model import GroupedSourceModel
from src.domain.repository.source_repository import SourceRepository


class GetGroupedSourcesUsecase:
    def __init__(self, source_repository: SourceRepository):
        self._source_repository = source_repository

    async def execute(self) -> List[GroupedSourceModel]:
        """
        Get sources grouped by type and url, with the minimum notification period
        and the earliest last_hit_datetime.
        """
        return (
            await self._source_repository.get_grouped_sources_by_notification_period()
        )
