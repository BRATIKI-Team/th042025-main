from telethon import TelegramClient as TelethonTelegramClient


class TelegramClient:
    def __init__(self, client: TelethonTelegramClient) -> None:
        self._client = client

    async def __enter__(self) -> None:
        await self._client.connect()

    async def __exit__(self) -> None:
        await self._client.disconnect()

    @property
    def engine(self) -> TelethonTelegramClient:
        return self._client
