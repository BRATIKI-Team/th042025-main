from src.application.dto.bot_light_response import BotLightResponse
from src.application.mapper.bot_mapper import BotMapper
from src.domain.repository.bot_repository import BotRepository


class GetAllBotsUsecase:
    def __init__(self, bot_repository: BotRepository):
        self._bot_repository = bot_repository

    async def execute(self) -> list[BotLightResponse]:
        bots = await self._bot_repository.get_all_bots()

        return [BotMapper.to_light_response(bot) for bot in bots]
