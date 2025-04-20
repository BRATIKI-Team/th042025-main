import asyncio
from typing import Optional
from src.infrastructure.tg.telegram_client import TelegramClient
from src.infrastructure.config import config
from telethon import TelegramClient as TelethonTelegramClient



class TelegramClientFactory:
    """
    Factory for creating and managing TelegramClient instances.
    Implements Singleton pattern to ensure only one client instance exists.
    """
    _instance: Optional['TelegramClientFactory'] = None
    _client: Optional[TelegramClient] = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelegramClientFactory, cls).__new__(cls)
        return cls._instance

    async def get_client(self) -> TelegramClient:
        """
        Get or create a TelegramClient instance.
        Ensures the client is connected before returning.

        Returns:
            TelegramClient: Connected client instance
        """
        async with self._lock:
            if self._client is None:
                self._client = TelegramClient(
                    TelethonTelegramClient(
                        session=config.TELEGRAM_SESSION_FILE,
                        api_id=config.TELEGRAM_API_ID,
                        api_hash=config.TELEGRAM_API_HASH,
                        request_retries=config.TELEGRAM_RETRY_COUNT,
                        retry_delay=config.TELEGRAM_RETRY_DELAY,
                        timeout=config.TELEGRAM_REQUEST_TIMEOUT,
                        connection_retries=config.TELEGRAM_CONNECTION_RETRIES,
                        auto_reconnect=config.TELEGRAM_AUTO_RECONNECT,
                        flood_sleep_threshold=config.TELEGRAM_FLOOD_SLEEP_THRESHOLD,
                        receive_updates=config.TELEGRAM_RECEIVE_UPDATES,
                        device_model=config.TELEGRAM_DEVICE_MODEL,
                        system_version=config.TELEGRAM_SYSTEM_VERSION,
                        app_version=config.TELEGRAM_APP_VERSION,
                        lang_code=config.TELEGRAM_LANG_CODE,
                        system_lang_code=config.TELEGRAM_SYSTEM_LANG_CODE,
                    )
                )
                await self._client.engine.connect()
            return self._client

    async def close(self):
        """
        Close the client connection if it exists.
        """
        async with self._lock:
            if self._client is not None:
                await self._client.engine.disconnect()
                self._client = None 