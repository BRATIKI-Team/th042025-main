from src.application.dto.create_bot_request import CreateBotRequest
from src.domain.repository.bot_repository import BotRepository


class CreateBotUsecase:
    def __init__(self, repository: BotRepository):
        self._repository = repository

    async def execute(self, request: CreateBotRequest) -> int:
        return await self._repository.create_bot(
            user_id=request.user_id,
            name=request.name,
            period=request.notification_period,
        )
