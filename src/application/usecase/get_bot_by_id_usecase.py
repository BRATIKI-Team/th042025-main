from typing import Optional

from src.domain.model.bot_model import BotModel
from src.domain.repository.bot_repository import BotRepository


class GetBotByIdUsecase:
    """
    Usecase for getting a bot by its ID.
    """
    
    def __init__(
        self,
        bot_repository: BotRepository
    ):
        self._bot_repository = bot_repository
    
    async def execute(self, bot_id: int) -> Optional[BotModel]:
        """
        Execute the usecase.
        
        Args:
            bot_id: The ID of the bot to get
            
        Returns:
            Optional[BotModel]: The bot model, or None if not found
        """
        return await self._bot_repository.read_by_id(bot_id) 