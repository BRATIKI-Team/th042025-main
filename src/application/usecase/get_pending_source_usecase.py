from src.domain.enum.source_status_enum import SourceStatus
from src.domain.model.source_model import SourceModel
from src.domain.repository.source_repository import SourceRepository


class GetPendingSourceUsecase:
    def __init__(self, source_repository: SourceRepository):
        self.source_repository = source_repository

    async def execute(self) -> SourceModel | None:
        return await self.source_repository.get_source_by_status(
            status=SourceStatus.PENDING
        )
