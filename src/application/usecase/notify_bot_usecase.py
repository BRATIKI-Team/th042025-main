from typing import List
import logging
from datetime import datetime

from aiogram import Bot

from src.application.agents.summary_workflow import SummaryWorkflow
from src.application.services import IndexService
from src.domain.model.message_model import MessageModel
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.message_repository import MessageRepository
from src.domain.repository.user_bot_repository import UserBotRepository
from src.infrastructure.config import config


logger = logging.getLogger(__name__)


class NotifyBotUsecase:
    """
    Usecase for notifying a bot about new messages.
    """

    def __init__(
        self,
        bot_repository: BotRepository,
        user_bot_repository: UserBotRepository,
        message_repository: MessageRepository,
        index_service: IndexService,
    ):
        self._bot_repository = bot_repository
        self._user_bot_repository = user_bot_repository
        self._message_repository = message_repository
        self._workflow = SummaryWorkflow(index_service=index_service)

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

        messages = await self._message_repository.read_by_bot_and_filter_by_created(
            bot.id, bot.last_notified_at
        )

        summrizedMessages = await self._workflow.start_workflow(
            bot.id, bot.description.value, messages
        )

        # This could involve sending a message to a Telegram bot,
        # posting to a webhook, etc.

        # Получаем список пользователей для этого бота
        user_ids = await self._user_bot_repository.get_users_by_bot_id(bot_id)
        if not user_ids:
            logger.warning(f"No users found for bot {bot_id}")
            return

        aiogram_bot = Bot(token=bot.token.value)

        try:
            for message in summrizedMessages:
                message_text = message.title + "\n\n" + message.content

                for user_id in user_ids:
                    try:
                        await aiogram_bot.send_message(
                            chat_id=user_id, text=message_text, parse_mode="HTML"
                        )
                        logger.info(
                            f"Sent notification to user {user_id} for bot {bot_id}"
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to send message to user {user_id}: {str(e)}"
                        )

            # Обновляем время последнего уведомления
            await self._bot_repository.update_last_notified_at(bot_id, datetime.now())

        except Exception as e:
            logger.error(f"Error in notify_bot_usecase: {str(e)}")
            raise e
        finally:
            # Закрываем сессию бота
            await aiogram_bot.session.close()
