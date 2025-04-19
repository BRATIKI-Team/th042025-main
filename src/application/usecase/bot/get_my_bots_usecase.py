from src.domain.model.bot_model import BotModel
from src.domain.model.pagination_model import PaginationModel
from src.domain.repository.bot_repository import BotRepository


class GetMyBotsUsecase:
    def __init__(self, bot_repository: BotRepository):
        self._bot_repository = bot_repository

    async def execute(
        self, user_id: int, page: int, page_size: int = 1
    ) -> PaginationModel[BotModel]:
        return await self._bot_repository.get_my_bots(
            user_id=user_id, page=page, page_size=page_size
        )
