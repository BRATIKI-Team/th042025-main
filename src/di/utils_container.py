from dishka import FromDishka, Provider, Scope, provide
from telethon import TelegramClient as TelethonTelegramClient

from src.infrastructure.config import config
from src.infrastructure.tg.telegram_client import TelegramClient


class UtilsContainer(Provider):
    @provide(scope=Scope.APP)
    def provide_telethon_telegram_client(self) -> TelethonTelegramClient:
        return TelethonTelegramClient(
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

    @provide(scope=Scope.APP)
    def provide_tg_client(
        self, client: FromDishka[TelethonTelegramClient]
    ) -> TelegramClient:
        return TelegramClient(client=client.value)
