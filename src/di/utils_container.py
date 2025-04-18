from dishka import Provider, Scope, provide
from telethon import TelegramClient

from src.infrastructure.config import config


class UtilsContainer(Provider):
    @provide(scope=Scope.APP)
    def provide_telegram_client(self) -> TelegramClient:
        return TelegramClient(
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
