from typing import List
from datetime import datetime

from src.application.usecase.get_bot_by_id_usecase import GetBotByIdUsecase
from src.application.usecase.update_bot_last_notified_usecase import (
    UpdateBotLastNotifiedUsecase,
)
from src.domain.model.message_model import MessageModel
from src.domain.repository import BotRepository
from src.domain.repository.message_repository import MessageRepository


class NotifyBotUsecase:
    """
    Usecase for notifying a bot about new messages.
    """

    def __init__(
            self,
            bot_repository: BotRepository,
            message_repository: MessageRepository,
    ):
        self._bot_repository = bot_repository
        self._message_repository = message_repository

    async def execute(self, bot_id: int) -> None:
        """
        Execute the usecase.

        Args:
            bot_id: The ID of the bot to notify
            messages: The messages to notify about
        """
        # Get the bot
        bot = await self._bot_repository.read_by_id(bot_id)
        if not bot:
            return
        
        messages = await self._message_repository.read_by_bot_and_filter_by_created(bot.id, bot.last_notified_at)
        # This could involve sending a message to a Telegram bot,
        # posting to a webhook, etc.

        # For now, just print the messages
        print(f"Notifying bot {bot_id} about {len(messages)} messages:")
        for message in messages:
            print(f"  - {message.content[:50]}...")

        # Update the bot's last_notified_at
        await self._bot_repository.update_last_notified_at(bot_id, datetime.now())
