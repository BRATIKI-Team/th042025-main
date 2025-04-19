from src.domain.enum.source_status_enum import SourceStatus
from src.domain.model.pagination_model import PaginationModel
from src.domain.model.source_model import SourceModel
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.source_repository import SourceRepository


class GetBotSourcesUsecase:
    def __init__(
        self, source_repository: SourceRepository, bot_repository: BotRepository
    ):
        self._source_repository = source_repository
        self._bot_repository = bot_repository

    async def execute(
        self, bot_id: int, status: SourceStatus, page: int, page_size: int = 1
    ) -> PaginationModel[SourceModel]:
        pagination = await self._source_repository.get_bot_sources(
            bot_id, status, page, page_size
        )

        if len(pagination.items) != 0 or status != SourceStatus.PENDING:
            return pagination

        bot = await self._bot_repository.read_by_id(bot_id)

        if bot is None:
            raise ValueError(f"Bot with id {bot_id} not found")

        await self._source_repository.search_sources(bot_id, bot.description.value)

        return await self._source_repository.get_bot_sources(
            bot_id, status, page, page_size
        )
