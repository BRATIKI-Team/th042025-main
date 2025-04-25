import asyncio

from aiogram import Bot
from src.di.container import init_container
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.bot_user_repository import BotUserRepository
from src.domain.repository.user_repository import UserRepository


async def check_updates(
    bot_user_repository: BotUserRepository,
    user_repository: UserRepository,
    bot_id: int,
    token: str,
    offset: int,
) -> int:
    bot = Bot(token=token)

    updates = await bot.get_updates(offset=offset, timeout=5)
    new_offset = offset

    for update in updates:
        if update.message and update.message.text == "/start":
            await user_repository.ensure_user_exists(
                user_id=update.message.from_user.id
            )
            await bot_user_repository.create_bot_user(
                bot_id=bot_id, user_id=update.message.from_user.id
            )
            await update.message.answer(
                "💌 Здравствуйте! Вы добавлены в систему. Теперь вы будете получать рассылку."
            )

            new_offset = max(new_offset, update.update_id + 1)

    await bot.session.close()

    return new_offset


async def main() -> None:
    container = init_container()

    bot_repository = await container.get(BotRepository)
    bot_user_repository = await container.get(BotUserRepository)
    user_repository = await container.get(UserRepository)

    offsets: dict[str, int] = {}

    while True:
        active_bots = await bot_repository.get_active_bots()

        for bot in active_bots:
            offset = offsets.get(bot.id, 0)
            new_offset = await check_updates(
                bot_user_repository=bot_user_repository,
                user_repository=user_repository,
                bot_id=bot.id,
                token=bot.token.value,
                offset=offset,
            )
            offsets[bot.id] = new_offset

        await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(main())
