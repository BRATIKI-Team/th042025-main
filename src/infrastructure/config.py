from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Class configuration
    """

    # Telegram
    TG_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
