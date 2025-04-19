from src.domain.repository.bot_repository import BotRepository


class IsTokenUniqueUsecase:
    def __init__(self, bot_repository: BotRepository):
        self._bot_repository = bot_repository

    async def execute(self, token: str) -> bool:
        return await self._bot_repository.get_bot_by_token(token) is None
