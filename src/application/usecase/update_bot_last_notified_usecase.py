from datetime import datetime

from src.domain.repository.bot_repository import BotRepository


class UpdateBotLastNotifiedUsecase:
    """
    Usecase for updating a bot's last_notified_at timestamp.
    """
    
    def __init__(
        self,
        bot_repository: BotRepository
    ):
        self._bot_repository = bot_repository
    
    async def execute(self, bot_id: int, last_notified_at: datetime) -> None:
        """
        Execute the usecase.
        
        Args:
            bot_id: The ID of the bot to update
            last_notified_at: The new timestamp
        """
        await self._bot_repository.update_last_notified_at(bot_id, last_notified_at) 