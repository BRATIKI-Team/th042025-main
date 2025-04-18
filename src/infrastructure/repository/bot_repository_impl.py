from src.domain.repository.bot_repository import BotRepository
from src.infrastructure.dao.bot_dao import BotDAO


class BotRepositoryImpl(BotRepository):
    async def has_bot(self, user_id: int) -> bool:
        dao = await BotDAO.objects().get(BotDAO.user_id == user_id).first()

        return dao is not None
