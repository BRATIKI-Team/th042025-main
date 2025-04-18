import asyncio
from telethon.errors import SessionPasswordNeededError

from src.di.container import init_container
from src.infrastructure.tg.telegram_client import TelegramClient


async def init_parser() -> None:
    container = init_container()

    telegram_client = await container.get(TelegramClient)

    async with telegram_client:
        if not await telegram_client.engine.is_user_authorized():
            phone = input("Enter your phone number: ")
            await telegram_client.engine.send_code_request(phone=phone)

            code = input("Enter the code: ")
            await telegram_client.engine.sign_in(phone=phone, code=code)

            try:
                await telegram_client.engine.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = input("Please enter your 2FA password: ")
                await telegram_client.engine.sign_in(password=password)


if __name__ == "__main__":
    asyncio.run(init_parser())
