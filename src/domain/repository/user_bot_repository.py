from abc import ABC, abstractmethod
from typing import List


class UserBotRepository(ABC):
    @abstractmethod
    async def get_users_by_bot_id(self, bot_id: int) -> List[int]:
        """
        Get all user IDs associated with a bot.
        
        Args:
            bot_id: The ID of the bot
            
        Returns:
            List[int]: List of user IDs
        """
        pass 