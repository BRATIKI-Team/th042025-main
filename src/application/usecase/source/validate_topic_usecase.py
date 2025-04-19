from src.domain.repository.source_repository import SourceRepository


class ValidateTopicUsecase:
    def __init__(self, source_repository: SourceRepository):
        self._source_repository = source_repository

    async def execute(self, topic: str) -> bool:
        return await self._source_repository.validate_topic(topic=topic)
