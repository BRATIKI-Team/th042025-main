from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import Dict, Optional


class Config(BaseSettings):
    """
    Class configuration
    """

    # Telegram Client
    TELEGRAM_TOKEN: SecretStr

    # Telegram Parser
    TELEGRAM_SESSION_FILE: str = "session/telegram"
    TELEGRAM_API_ID: str = "17859970"
    TELEGRAM_API_HASH: str = "34354cc46b3fbc4a64f765570a8e9666"
    TELEGRAM_RETRY_COUNT: int = 3
    TELEGRAM_RETRY_DELAY: int = 1
    TELEGRAM_REQUEST_TIMEOUT: int = 30
    TELEGRAM_CONNECTION_RETRIES: int = 5
    TELEGRAM_AUTO_RECONNECT: bool = True
    TELEGRAM_FLOOD_SLEEP_THRESHOLD: int = 60
    TELEGRAM_RECEIVE_UPDATES: bool = False
    TELEGRAM_APP_VERSION: str = "8.11.0"
    TELEGRAM_DEVICE_MODEL: str = "Desktop"
    TELEGRAM_SYSTEM_VERSION: str = "Windows 10"
    TELEGRAM_LANG_CODE: str = "en"
    TELEGRAM_SYSTEM_LANG_CODE: str = "en"
    TELEGRAM_DOWNLOAD_PATH: str = "data"
    TELEGRAM_PARSER_MAX_WORKERS: int = 5

    # Database
    DATABASE_PATH: str = "db/db.sqlite"
    CHROMADB_PATH: str = "db/chroma"
    MIGRATIONS_PATH: str = "src/infrastructure/database/migrations"

    # OPENAI
    OPENAI_API_KEY: SecretStr
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"

    # Logs
    LOGS_FILES_PATH: str = "logs"
    LOGS_BACKUP_COUNT: int = 7

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
