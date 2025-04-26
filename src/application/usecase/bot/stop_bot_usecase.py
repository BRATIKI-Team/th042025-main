from src.domain.enum.bot_status_enum import BotStatus
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.telegram_repository import TelegramRepository


class StopBotUsecase:
    def __init__(
        self, bot_repository: BotRepository, telegram_repository: TelegramRepository
    ):
        self._bot_repository = bot_repository
        self._telegram_repository = telegram_repository

    async def execute(self, bot_id: int) -> None:
        bot = await self._bot_repository.read_by_id(bot_id)

        if bot is None:
            raise ValueError("Bot not found")

        await self._bot_repository.update_bot_status(bot_id, BotStatus.INACTIVE)
        await self._telegram_repository.stop_bot_listening(bot.token.value)
