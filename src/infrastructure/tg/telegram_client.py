from telethon import TelegramClient as TelethonTelegramClient


class TelegramClient:
    def __init__(self, client: TelethonTelegramClient) -> None:
        self._client = client

    @property
    def engine(self) -> TelethonTelegramClient:
        return self._client
