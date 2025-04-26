import asyncio
from telethon.errors import SessionPasswordNeededError

from src.di.container import init_container
from src.infrastructure.tg.telegram_client_factory import TelegramClientFactory


async def init_parser(session_file: str | None = None) -> None:
    container = init_container()

    telegram_client_factory = await container.get(TelegramClientFactory)
    telegram_client = await telegram_client_factory.get_client(
        session_file=session_file
    )

    if not await telegram_client.engine.is_user_authorized():
        phone = input("Enter your phone number: ")
        await telegram_client.engine.send_code_request(phone=phone)

        code = input("Enter the code: ")
        try:
            await telegram_client.engine.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input("Please enter your 2FA password: ")
            await telegram_client.engine.sign_in(password=password)


if __name__ == "__main__":
    import sys

    session_file: str | None = None

    if len(sys.argv) > 1:
        session_file = sys.argv[1]

    asyncio.run(init_parser(session_file=session_file))
