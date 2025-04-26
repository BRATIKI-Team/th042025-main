import asyncio

from src.di.container import init_container
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.telegram_repository import TelegramRepository


async def main() -> None:
    container = init_container()

    bot_repository = await container.get(BotRepository)
    telegram_repository = await container.get(TelegramRepository)

    active_bots = await bot_repository.get_active_bots()

    for bot in active_bots:
        await telegram_repository.start_bot_listening(
            bot_id=bot.id, bot_token=bot.token.value
        )


if __name__ == "__main__":
    asyncio.run(main())
