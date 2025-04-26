from typing import List

from src.domain.model.bot_model import BotModel
from src.domain.repository import BotRepository


class GetActiveBotsUsecase:
    def __init__(self, bot_repository: BotRepository):
        self._bot_repository = bot_repository

    async def execute(self) -> List[BotModel]:
        return await self._bot_repository.get_active_bots()
