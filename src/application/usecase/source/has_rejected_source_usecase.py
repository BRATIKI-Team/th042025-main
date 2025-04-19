from src.domain.repository.source_repository import SourceRepository


class HasRejectedSourceUsecase:
    def __init__(self, source_repository: SourceRepository):
        self._source_repository = source_repository

    async def execute(self, bot_id: int) -> bool:
        return await self._source_repository.has_rejected_source(bot_id)
