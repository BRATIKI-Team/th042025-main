from src.application.dto.bot_detail_response import BotDetailResponse
from src.application.mapper.bot_mapper import BotMapper
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.bot_user_repository import BotUserRepository
from src.domain.repository.message_repository import MessageRepository
from src.domain.repository.source_repository import SourceRepository


class GetDetailBotUsecase:
    def __init__(
        self,
        bot_repository: BotRepository,
        source_repository: SourceRepository,
        bot_user_repository: BotUserRepository,
        message_repository: MessageRepository,
    ):
        self._bot_repository = bot_repository
        self._source_repository = source_repository
        self._bot_user_repository = bot_user_repository
        self._message_repository = message_repository

    async def execute(self, bot_id: int) -> BotDetailResponse:
        bot = await self._bot_repository.read_by_id(bot_id)

        if bot is None:
            raise ValueError(f"Bot not found: {bot_id}")

        sources = await self._source_repository.get_by_bot_id(bot_id)
        users_count = await self._bot_user_repository.get_users_count(bot_id)
        metrics = await self._message_repository.get_metrics(
            [source.id for source in sources]
        )

        return BotMapper.to_detail_response(bot, sources, users_count, metrics)
