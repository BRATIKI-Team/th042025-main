from src.application.dto.create_bot_request import CreateBotRequest
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.user_repository import UserRepository


class CreateBotUsecase:
    def __init__(self, bot_repository: BotRepository, user_repository: UserRepository):
        self._bot_repository = bot_repository
        self._user_repository = user_repository

    async def execute(self, request: CreateBotRequest) -> int:
        await self._user_repository.ensure_user_exists(user_id=request.user_id)

        return await self._bot_repository.create_bot(
            user_id=request.user_id,
            name=request.name,
            description=request.description,
            period=request.period,
            token=request.token,
        )
