from telethon import TelegramClient as TelethonTelegramClient


class TelegramClient:
    def __init__(self, client: TelethonTelegramClient) -> None:
        self._client = client

    async def __aenter__(self) -> None:
        await self._client.connect()

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._client.disconnect()

    @property
    def engine(self) -> TelethonTelegramClient:
        return self._client
