from typing import List

from src.domain.repository.user_bot_repository import UserBotRepository
from src.infrastructure.dao import BotUserDAO
from src.infrastructure.dao.bot_dao import BotDAO


class UserBotRepositoryImpl(UserBotRepository):
    async def get_users_by_bot_id(self, bot_id: int) -> List[int]:
        """
        Get all user IDs associated with a bot.

        Args:
            bot_id: The ID of the bot

        Returns:
            List[int]: List of user IDs
        """
        # Получаем бота по ID
        botUsers = await BotUserDAO.select().where(BotUserDAO.bot_id == bot_id)

        # Возвращаем user_id бота
        return [botUser["user_id"] for botUser in botUsers]
