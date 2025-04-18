import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from src.di.container import init_container


async def init_parser() -> None:
    container = init_container()

    telegram_client = await container.get(TelegramClient)

    await telegram_client.connect()

    if not await telegram_client.is_user_authorized():
        phone = input("Enter your phone number: ")
        await telegram_client.send_code_request(phone=phone)

        code = input("Enter the code: ")
        await telegram_client.sign_in(phone=phone, code=code)

        try:
            await telegram_client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input("Please enter your 2FA password: ")
            await telegram_client.sign_in(password=password)

    await telegram_client.disconnect()


if __name__ == "__main__":
    asyncio.run(init_parser())
