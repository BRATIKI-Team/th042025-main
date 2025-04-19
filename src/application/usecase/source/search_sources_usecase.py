import logging
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.source_repository import SourceRepository


class SearchSourcesUsecase:
    def __init__(
        self, source_repository: SourceRepository, bot_repository: BotRepository
    ):
        self._source_repository = source_repository
        self._bot_repository = bot_repository

    async def execute(self, bot_id: int) -> None:
        bot = await self._bot_repository.read_by_id(bot_id=bot_id)

        if bot is None:
            return logging.warning(f"Bot with id {bot_id} not found")

        await self._source_repository.search_sources(
            bot_id=bot_id, topic=bot.description.value
        )
