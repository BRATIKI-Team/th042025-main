from src.domain.enum.source_status_enum import SourceStatus
from src.domain.repository.source_repository import SourceRepository


class RejectSourceUsecase:
    def __init__(self, source_repository: SourceRepository):
        self._source_repository = source_repository

    async def execute(self, source_id: int) -> None:
        await self._source_repository.change_status(
            id=source_id, status=SourceStatus.REJECTED
        )
