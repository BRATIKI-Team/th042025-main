from dishka import FromDishka, Provider, Scope, provide

from src.application.usecase.create_bot_usecase import CreateBotUsecase
from src.application.usecase.get_bot_by_id_usecase import GetBotByIdUsecase
from src.application.usecase.get_grouped_sources_usecase import GetGroupedSourcesUsecase
from src.application.usecase.get_pending_source_usecase import GetPendingSourceUsecase
from src.application.usecase.get_source_messages_usecase import GetSourceMessagesUsecase
from src.application.usecase.has_bot_usecase import HasBotUsecase
from src.application.usecase.notify_bot_usecase import NotifyBotUsecase
from src.application.usecase.update_bot_last_notified_usecase import UpdateBotLastNotifiedUsecase
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
from src.domain.repository.message_repository import MessageRepository
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
    def get_grouped_sources_usecase(
            self, source_repository: FromDishka[SourceRepository]
    ) -> GetGroupedSourcesUsecase:
        return GetGroupedSourcesUsecase(source_repository=source_repository)

    @provide(scope=Scope.APP)
    def get_source_messages_usecase(
            self,
            source_repository: FromDishka[SourceRepository],
            message_repository: FromDishka[MessageRepository],
            telegram_repository: FromDishka[TelegramRepository]
    ) -> GetSourceMessagesUsecase:
        return GetSourceMessagesUsecase(
            source_repository=source_repository,
            message_repository=message_repository,
            telegram_repository=telegram_repository,
        )

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
            self, bot_repository: FromDishka[BotRepository]

    @provide(scope=Scope.APP)
    def get_bot_by_id_usecase(
            self, bot_repository: FromDishka[BotRepository]
    ) -> GetBotByIdUsecase:
        return GetBotByIdUsecase(bot_repository=bot_repository)

    @provide(scope=Scope.APP)
    def update_bot_last_notified_usecase(
            self, bot_repository: FromDishka[BotRepository]
    ) -> UpdateBotLastNotifiedUsecase:
        return UpdateBotLastNotifiedUsecase(bot_repository=bot_repository)

    @provide(scope=Scope.APP)
    def notify_bot_usecase(
            self,
            get_bot_by_id_usecase: FromDishka[GetBotByIdUsecase],
            update_bot_last_notified_usecase: FromDishka[UpdateBotLastNotifiedUsecase]
    ) -> NotifyBotUsecase:
        return NotifyBotUsecase(
            get_bot_by_id_usecase=get_bot_by_id_usecase,
            update_bot_last_notified_usecase=update_bot_last_notified_usecase
        )
