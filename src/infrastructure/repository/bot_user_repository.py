from src.domain.repository.bot_user_repository import BotUserRepository
from src.infrastructure.dao.bot_user_dao import BotUserDAO


class BotUserRepositoryImpl(BotUserRepository):
    async def create_bot_user(self, bot_id: int, user_id: int) -> None:
        dao = (
            await BotUserDAO.objects()
            .get((BotUserDAO.bot_id == bot_id) & (BotUserDAO.user_id == user_id))
            .first()
        )

        if dao is not None:
            return

        await BotUserDAO.objects().create(bot_id=bot_id, user_id=user_id)
