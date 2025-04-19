import logging
from src.domain.enum.bot_status_enum import BotStatus
from src.domain.repository.bot_repository import BotRepository


class DeleteBotUsecase:
    def __init__(self, bot_repository: BotRepository):
        self._bot_repository = bot_repository

    async def execute(self, bot_id: int) -> None:
        bot = await self._bot_repository.read_by_id(bot_id)

        if bot is None:
            return logging.warning(f"Bot with id {bot_id} not found")

        if bot.status.value == BotStatus.ACTIVE.value:
            return logging.warning(f"Bot with id {bot_id} is active")

        await self._bot_repository.delete_bot(bot_id)
