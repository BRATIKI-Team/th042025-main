from dishka import FromDishka, Provider, Scope, provide

from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.source_repository import SourceRepository
from src.domain.repository.telegram_repository import TelegramRepository
from src.infrastructure.repository.bot_repository_impl import BotRepositoryImpl
from src.infrastructure.repository.source_repository_impl import SourceRepositoryImpl
from src.infrastructure.repository.telegram_repository_impl import (
    TelegramRepositoryImpl,
)
from src.infrastructure.tg.telegram_client import TelegramClient
from src.infrastructure.config import config


class RepositoryContainer(Provider):
    @provide(scope=Scope.APP)
    def bot_repository(self) -> BotRepository:
        return BotRepositoryImpl()

    @provide(scope=Scope.APP)
    def source_repository(self) -> SourceRepository:
        return SourceRepositoryImpl()

    @provide(scope=Scope.APP)
    def telegram_repository(
        self, tg_client: FromDishka[TelegramClient]
    ) -> TelegramRepository:
        return TelegramRepositoryImpl(
            tg_client=tg_client,
            download_path=config.TELEGRAM_DOWNLOAD_PATH,
            max_workers=config.TELEGRAM_PARSER_MAX_WORKERS,
        )
