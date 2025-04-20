from dishka import FromDishka, Provider, Scope, provide

from src.application.agents.source_searcher import SourceSearcherAgent
from src.application.agents.topic_validator.topic_validator_agent import (
    TopicValidatorAgent,
)
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.bot_user_repository import BotUserRepository
from src.domain.repository.chroma_repository import ChromaRepository
from src.domain.repository.message_repository import MessageRepository
from src.domain.repository.source_repository import SourceRepository
from src.domain.repository.summary_repository import SummaryRepository
from src.domain.repository.telegram_repository import TelegramRepository
from src.domain.repository.user_repository import UserRepository
from src.domain.repository.user_bot_repository import UserBotRepository
from src.infrastructure.repository.bot_repository_impl import BotRepositoryImpl
from src.infrastructure.repository.bot_user_repository import BotUserRepositoryImpl
from src.infrastructure.repository.message_repository_impl import MessageRepositoryImpl
from src.infrastructure.repository.chroma_repository_impl import ChromaRepositoryImpl
from src.infrastructure.repository.source_repository_impl import SourceRepositoryImpl
from src.infrastructure.repository.telegram_repository_impl import (
    TelegramRepositoryImpl,
)
from src.infrastructure.repository.summary_repository_impl import SummaryRepositoryImpl
from src.infrastructure.repository.user_repository_impl import UserRepositoryImpl
from src.infrastructure.repository.user_bot_repository_impl import UserBotRepositoryImpl
from src.infrastructure.tg.telegram_client import TelegramClient
from src.infrastructure.config import config


class RepositoryContainer(Provider):
    @provide(scope=Scope.APP)
    def bot_repository(self) -> BotRepository:
        return BotRepositoryImpl()

    @provide(scope=Scope.APP)
    def source_repository(
        self,
        validate_topic_agent: FromDishka[TopicValidatorAgent],
        search_sources_agent: FromDishka[SourceSearcherAgent],
        telegram_repository: FromDishka[TelegramRepository],
    ) -> SourceRepository:
        return SourceRepositoryImpl(
            validate_topic_agent=validate_topic_agent,
            search_sources_agent=search_sources_agent,
            telegram_repository=telegram_repository,
        )

    @provide(scope=Scope.APP)
    def message_repository(self) -> MessageRepository:
        return MessageRepositoryImpl()

    @provide(scope=Scope.APP)
    def telegram_repository(
        self, tg_client: FromDishka[TelegramClient]
    ) -> TelegramRepository:
        return TelegramRepositoryImpl(
            tg_client=tg_client,
            download_path=config.TELEGRAM_DOWNLOAD_PATH,
            max_workers=config.TELEGRAM_PARSER_MAX_WORKERS,
        )

    @provide(scope=Scope.APP)
    def chroma_repository(self) -> ChromaRepository:
        return ChromaRepositoryImpl()

    @provide(scope=Scope.APP)
    def user_repository(self) -> UserRepository:
        return UserRepositoryImpl()

    @provide(scope=Scope.APP)
    def user_bot_repository(self) -> UserBotRepository:
        return UserBotRepositoryImpl()

    @provide(scope=Scope.APP)
    def bot_user_repository(self) -> BotUserRepository:
        return BotUserRepositoryImpl()

    @provide(scope=Scope.APP)
    def summary_repository(self) -> SummaryRepository:
        return SummaryRepositoryImpl()
