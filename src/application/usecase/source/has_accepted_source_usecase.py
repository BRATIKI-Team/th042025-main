from src.domain.repository.source_repository import SourceRepository


class HasAcceptedSourceUsecase:
    def __init__(self, source_repository: SourceRepository):
        self._source_repository = source_repository

    async def execute(self, bot_id: int) -> bool:
        return await self._source_repository.has_accepted_source(bot_id)
