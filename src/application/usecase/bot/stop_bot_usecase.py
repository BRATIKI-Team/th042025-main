from src.domain.enum.bot_status_enum import BotStatus
from src.domain.repository.bot_repository import BotRepository


class StopBotUsecase:
    def __init__(self, bot_repository: BotRepository):
        self._bot_repository = bot_repository

    async def execute(self, bot_id: int) -> None:
        await self._bot_repository.update_bot_status(bot_id, BotStatus.INACTIVE)
