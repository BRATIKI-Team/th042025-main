import logging
from aiogram import Bot
from src.domain.repository.bot_repository import BotRepository
from aiogram.types import Update

from src.domain.repository.bot_user_repository import BotUserRepository
from src.domain.repository.user_repository import UserRepository


class WebhookUsecase:
    def __init__(
        self,
        bot_repository: BotRepository,
        user_repository: UserRepository,
        bot_user_repository: BotUserRepository,
    ):
        self._bot_repository = bot_repository
        self._user_repository = user_repository
        self._bot_user_repository = bot_user_repository

    async def execute(self, bot_id: int, update: Update) -> None:
        bot_model = await self._bot_repository.read_by_id(bot_id)

        if bot_model is None:
            raise ValueError("Bot not found")

        bot = Bot(token=bot_model.token.value)

        if not update.message or update.message.text != "/start":
            return

        await self._user_repository.ensure_user_exists(
            user_id=update.message.from_user.id
        )
        await self._bot_user_repository.create_bot_user(
            bot_id=bot_id, user_id=update.message.from_user.id
        )

        try:
            await bot.send_message(
                chat_id=update.message.chat.id,
                text="💌 Здравствуйте! Вы добавлены в систему. Теперь вы будете получать рассылку.",
            )
        except Exception as e:
            logging.error(f"Error sending message: {e}")
        finally:
            await bot.session.close()
