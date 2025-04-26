import asyncio
import logging
import os
from typing import Optional
from src.infrastructure.tg.telegram_client import TelegramClient
from src.infrastructure.config import config
from telethon import TelegramClient as TelethonTelegramClient
from telethon.sessions import SQLiteSession

logger = logging.getLogger(__name__)


class TelegramClientFactory:
    """
    Factory for creating and managing TelegramClient instances.
    Implements Singleton pattern to ensure only one client instance exists.
    """

    _instance: Optional["TelegramClientFactory"] = None
    _client: Optional[TelegramClient] = None
    _lock = asyncio.Lock()
    _max_retries = 3
    _retry_delay = 1  # seconds

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelegramClientFactory, cls).__new__(cls)
        return cls._instance

    async def get_client(self, session_file: str | None = None) -> TelegramClient:
        """
        Get or create a TelegramClient instance.
        Ensures the client is connected before returning.

        Returns:
            TelegramClient: Connected client instance
        """
        async with self._lock:
            if self._client is None:
                self._client = await self._create_client(
                    session_file=session_file or config.TELEGRAM_SESSION_FILE
                )
            return self._client

    async def _create_client(self, session_file: str) -> TelegramClient:
        """
        Create a new TelegramClient instance.
        """

        client = TelegramClient(
            TelethonTelegramClient(
                session=session_file,
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

        for attempt in range(self._max_retries):
            try:
                await client.engine.connect()
                if not await client.engine.is_user_authorized():
                    logger.warning("Telegram client is not authorized")
                return client
            except Exception as e:
                if attempt == self._max_retries - 1:
                    logger.error(
                        f"Failed to connect to Telegram after {self._max_retries} attempts: {str(e)}"
                    )
                    raise
                logger.warning(
                    f"Failed to connect to Telegram (attempt {attempt + 1}/{self._max_retries}): {str(e)}"
                )
                await asyncio.sleep(self._retry_delay)
        raise Exception("Failed to connect to Telegram")

    async def close(self):
        """
        Close the client connection if it exists.
        """
        async with self._lock:
            if self._client is not None:
                try:
                    await self._client.engine.disconnect()
                except Exception as e:
                    logger.error(f"Error disconnecting Telegram client: {str(e)}")
                finally:
                    self._client = None
