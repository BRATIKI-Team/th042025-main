from src.domain.repository.bot_repository import BotRepository


class HasBotUsecase:
    def __init__(self, bot_repository: BotRepository):
        self._bot_repository = bot_repository

    async def execute(self, user_id: int) -> bool:
        return await self._bot_repository.has_bot(user_id=user_id)
