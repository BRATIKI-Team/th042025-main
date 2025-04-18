from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Class configuration
    """

    # Telegram
    TG_TOKEN: SecretStr

    # Database
    DATABASE_PATH: str = "db/db.sqlite"
    MIGRATIONS_PATH: str = "src/infrastructure/database/migrations"

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
