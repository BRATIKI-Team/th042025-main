import asyncio
from aiogram import Dispatcher, Bot
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from src.di.container import init_container
from src.infrastructure.config import config


async def main() -> None:
    bot = Bot(token=config.TG_TOKEN.get_secret_value())
    dp = Dispatcher()

    container = init_container(specific_providers=[AiogramProvider()])

    setup_dishka(container=container, router=dp, auto_inject=True)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    asyncio.run(main())
