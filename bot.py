import asyncio
from aiogram import Dispatcher, Bot
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from src.di.container import init_container
from src.infrastructure.config import config
from src.presentation.command.start_command import router as start_command_router
from src.presentation.screen.create_bot_screen import router as create_bot_screen_router
from src.presentation.screen.manage_bot_screen import router as manage_bot_screen_router
from src.presentation.screen.menu_screen import router as menu_screen_router


async def main() -> None:
    bot = Bot(token=config.TELEGRAM_TOKEN.get_secret_value())
    dp = Dispatcher()

    # Command routers
    dp.include_router(start_command_router)

    # Screen routers
    dp.include_router(menu_screen_router)
    dp.include_router(create_bot_screen_router)
    dp.include_router(manage_bot_screen_router)

    container = init_container(specific_providers=[AiogramProvider()])

    setup_dishka(container=container, router=dp, auto_inject=True)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    asyncio.run(main())
