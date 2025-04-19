from dishka import FromDishka, Provider, Scope, provide

from src.application.usecase.create_bot_usecase import CreateBotUsecase
from src.application.usecase.get_pending_source_usecase import GetPendingSourceUsecase
from src.application.usecase.has_bot_usecase import HasBotUsecase
from src.application.usecase.telegram_download_media_usecase import (
    TelegramDownloadMediaUsecase,
)
from src.application.usecase.telegram_get_channel_info_usecase import (
    TelegramGetChannelInfoUsecase,
)
from src.application.usecase.telegram_get_messages_usecase import (
    TelegramGetMessagesUsecase,
)
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.source_repository import SourceRepository
from src.domain.repository.telegram_repository import TelegramRepository
from src.domain.repository.user_repository import UserRepository


class UsecaseContainer(Provider):
    @provide(scope=Scope.APP)
    def has_bot_usecase(
        self, bot_repository: FromDishka[BotRepository]
    ) -> HasBotUsecase:
        return HasBotUsecase(bot_repository=bot_repository)

    @provide(scope=Scope.APP)
    def get_pending_source_usecase(
        self, source_repository: FromDishka[SourceRepository]
    ) -> GetPendingSourceUsecase:
        return GetPendingSourceUsecase(source_repository=source_repository)

    @provide(scope=Scope.APP)
    def telegram_get_channel_info_usecase(
        self, telegram_repository: FromDishka[TelegramRepository]
    ) -> TelegramGetChannelInfoUsecase:
        return TelegramGetChannelInfoUsecase(repository=telegram_repository)

    @provide(scope=Scope.APP)
    def telegram_get_messages_usecase(
        self, telegram_repository: FromDishka[TelegramRepository]
    ) -> TelegramGetMessagesUsecase:
        return TelegramGetMessagesUsecase(repository=telegram_repository)

    @provide(scope=Scope.APP)
    def telegram_download_media_usecase(
        self, telegram_repository: FromDishka[TelegramRepository]
    ) -> TelegramDownloadMediaUsecase:
        return TelegramDownloadMediaUsecase(repository=telegram_repository)

    @provide(scope=Scope.APP)
    def create_bot_usecase(
        self,
        bot_repository: FromDishka[BotRepository],
        user_repository: FromDishka[UserRepository],
    ) -> CreateBotUsecase:
        return CreateBotUsecase(
            bot_repository=bot_repository, user_repository=user_repository
        )
