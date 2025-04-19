from typing import List
from datetime import datetime

from src.application.usecase.get_bot_by_id_usecase import GetBotByIdUsecase
from src.application.usecase.update_bot_last_notified_usecase import UpdateBotLastNotifiedUsecase
from src.domain.model.bot_model import BotModel
from src.domain.model.message_model import MessageModel


class NotifyBotUsecase:
    """
    Usecase for notifying a bot about new messages.
    """
    
    def __init__(
        self,
        get_bot_by_id_usecase: GetBotByIdUsecase,
        update_bot_last_notified_usecase: UpdateBotLastNotifiedUsecase
    ):
        self._get_bot_by_id_usecase = get_bot_by_id_usecase
        self._update_bot_last_notified_usecase = update_bot_last_notified_usecase
    
    async def execute(self, bot_id: int, messages: List[MessageModel]) -> None:
        """
        Execute the usecase.
        
        Args:
            bot_id: The ID of the bot to notify
            messages: The messages to notify about
        """
        # Get the bot
        bot = await self._get_bot_by_id_usecase.execute(bot_id)
        if not bot:
            return
        
        # TODO: Implement actual notification logic here
        # This could involve sending a message to a Telegram bot,
        # posting to a webhook, etc.
        
        # For now, just print the messages
        print(f"Notifying bot {bot_id} about {len(messages)} messages:")
        for message in messages:
            print(f"  - {message.content[:50]}...")
        
        # Update the bot's last_notified_at
        await self._update_bot_last_notified_usecase.execute(bot_id, datetime.now()) 