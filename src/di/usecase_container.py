from dishka import FromDishka, Provider, Scope, provide

from src.application.services import IndexService
from src.application.usecase.bot.delete_bot_usecase import DeleteBotUsecase
from src.application.usecase.bot.get_active_bots_usecase import GetActiveBotsUsecase
from src.application.usecase.bot.get_all_bots_usecase import GetAllBotsUsecase
from src.application.usecase.bot.get_detail_bot_usecase import GetDetailBotUsecase
from src.application.usecase.bot.get_my_bots_usecase import GetMyBotsUsecase
from src.application.usecase.bot.is_token_unqiue_usecase import IsTokenUniqueUsecase
from src.application.usecase.bot.resume_bot_usecase import ResumeBotUsecase
from src.application.usecase.bot.stop_bot_usecase import StopBotUsecase
from src.application.usecase.bot.get_bot_by_id_usecase import GetBotByIdUsecase
from src.application.usecase.source.get_source_messages_usecase import (
    GetSourceMessagesUsecase,
)
from src.application.usecase.tg.notify_bot_usecase import NotifyBotUsecase
from src.application.usecase.source.accept_source_usecase import AcceptSourceUsecase
from src.application.usecase.source.get_bot_sources_usecase import GetBotSourcesUsecase
from src.application.usecase.source.has_accepted_source_usecase import (
    HasAcceptedSourceUsecase,
)
from src.application.usecase.source.has_rejected_source_usecase import (
    HasRejectedSourceUsecase,
)
from src.application.usecase.source.reject_source_usecase import RejectSourceUsecase
from src.application.usecase.source.search_sources_usecase import SearchSourcesUsecase
from src.application.usecase.tg.webhook_usecase import WebhookUsecase
from src.application.usecase.bot.create_bot_usecase import CreateBotUsecase
from src.application.usecase.source.get_pending_source_usecase import (
    GetPendingSourceUsecase,
)
from src.application.usecase.bot.has_bot_usecase import HasBotUsecase
from src.application.usecase.source.validate_topic_usecase import ValidateTopicUsecase
from src.application.usecase.tg.telegram_download_media_usecase import (
    TelegramDownloadMediaUsecase,
)
from src.application.usecase.tg.telegram_get_channel_info_usecase import (
    TelegramGetChannelInfoUsecase,
)
from src.application.usecase.tg.telegram_get_messages_usecase import (
    TelegramGetMessagesUsecase,
)
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.bot_user_repository import BotUserRepository
from src.domain.repository.message_repository import MessageRepository
from src.domain.repository.source_repository import SourceRepository
from src.domain.repository.telegram_repository import TelegramRepository
from src.domain.repository.user_bot_repository import UserBotRepository
from src.domain.repository.user_repository import UserRepository
from src.domain.repository.summary_repository import SummaryRepository


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
    def get_source_messages_usecase(
        self,
        source_repository: FromDishka[SourceRepository],
        message_repository: FromDishka[MessageRepository],
        telegram_repository: FromDishka[TelegramRepository],
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
        telegram_repository: FromDishka[TelegramRepository],
    ) -> CreateBotUsecase:
        return CreateBotUsecase(
            bot_repository=bot_repository,
            user_repository=user_repository,
            telegram_repository=telegram_repository,
        )

    @provide(scope=Scope.APP)
    def get_bot_by_id_usecase(
        self, bot_repository: FromDishka[BotRepository]
    ) -> GetBotByIdUsecase:
        return GetBotByIdUsecase(bot_repository=bot_repository)

    @provide(scope=Scope.APP)
    def notify_bot_usecase(
        self,
        bot_repository: FromDishka[BotRepository],
        user_bot_repository: FromDishka[UserBotRepository],
        message_repository: FromDishka[MessageRepository],
        summary_repository: FromDishka[SummaryRepository],
        telegram_repository: FromDishka[TelegramRepository],
        index_service: FromDishka[IndexService],
    ) -> NotifyBotUsecase:
        return NotifyBotUsecase(
            bot_repository=bot_repository,
            user_bot_repository=user_bot_repository,
            message_repository=message_repository,
            summary_repository=summary_repository,
            telegram_repository=telegram_repository,
            index_service=index_service,
        )

    @provide(scope=Scope.APP)
    def validate_topic_usecase(
        self, source_repository: FromDishka[SourceRepository]
    ) -> ValidateTopicUsecase:
        return ValidateTopicUsecase(source_repository=source_repository)

    @provide(scope=Scope.APP)
    def search_sources_usecase(
        self,
        source_repository: FromDishka[SourceRepository],
        bot_repository: FromDishka[BotRepository],
    ) -> SearchSourcesUsecase:
        return SearchSourcesUsecase(
            source_repository=source_repository, bot_repository=bot_repository
        )

    @provide(scope=Scope.APP)
    def accept_source_usecase(
        self, source_repository: FromDishka[SourceRepository]
    ) -> AcceptSourceUsecase:
        return AcceptSourceUsecase(source_repository=source_repository)

    @provide(scope=Scope.APP)
    def reject_source_usecase(
        self, source_repository: FromDishka[SourceRepository]
    ) -> RejectSourceUsecase:
        return RejectSourceUsecase(source_repository=source_repository)

    @provide(scope=Scope.APP)
    def get_my_bots_usecase(
        self, bot_repository: FromDishka[BotRepository]
    ) -> GetMyBotsUsecase:
        return GetMyBotsUsecase(bot_repository=bot_repository)

    @provide(scope=Scope.APP)
    def is_token_unique_usecase(
        self, bot_repository: FromDishka[BotRepository]
    ) -> IsTokenUniqueUsecase:
        return IsTokenUniqueUsecase(bot_repository=bot_repository)

    @provide(scope=Scope.APP)
    def delete_bot_usecase(
        self, bot_repository: FromDishka[BotRepository]
    ) -> DeleteBotUsecase:
        return DeleteBotUsecase(bot_repository=bot_repository)

    @provide(scope=Scope.APP)
    def resume_bot_usecase(
        self,
        bot_repository: FromDishka[BotRepository],
        telegram_repository: FromDishka[TelegramRepository],
    ) -> ResumeBotUsecase:
        return ResumeBotUsecase(
            bot_repository=bot_repository, telegram_repository=telegram_repository
        )

    @provide(scope=Scope.APP)
    def stop_bot_usecase(
        self,
        bot_repository: FromDishka[BotRepository],
        telegram_repository: FromDishka[TelegramRepository],
    ) -> StopBotUsecase:
        return StopBotUsecase(
            bot_repository=bot_repository, telegram_repository=telegram_repository
        )

    @provide(scope=Scope.APP)
    def has_rejected_source_usecase(
        self, source_repository: FromDishka[SourceRepository]
    ) -> HasRejectedSourceUsecase:
        return HasRejectedSourceUsecase(source_repository=source_repository)

    @provide(scope=Scope.APP)
    def get_bot_sources_usecase(
        self,
        source_repository: FromDishka[SourceRepository],
        bot_repository: FromDishka[BotRepository],
    ) -> GetBotSourcesUsecase:
        return GetBotSourcesUsecase(
            source_repository=source_repository, bot_repository=bot_repository
        )

    @provide(scope=Scope.APP)
    def has_accepted_source_usecase(
        self, source_repository: FromDishka[SourceRepository]
    ) -> HasAcceptedSourceUsecase:
        return HasAcceptedSourceUsecase(source_repository=source_repository)

    @provide(scope=Scope.APP)
    def get_detail_bot_usecase(
        self,
        bot_repository: FromDishka[BotRepository],
        source_repository: FromDishka[SourceRepository],
        bot_user_repository: FromDishka[BotUserRepository],
        summary_repository: FromDishka[SummaryRepository],
    ) -> GetDetailBotUsecase:
        return GetDetailBotUsecase(
            bot_repository=bot_repository,
            source_repository=source_repository,
            bot_user_repository=bot_user_repository,
            summary_repository=summary_repository,
        )

    @provide(scope=Scope.APP)
    def get_all_bots_usecase(
        self, bot_repository: FromDishka[BotRepository]
    ) -> GetAllBotsUsecase:
        return GetAllBotsUsecase(bot_repository=bot_repository)

    @provide(scope=Scope.APP)
    def webhook_usecase(
        self,
        bot_repository: FromDishka[BotRepository],
        user_repository: FromDishka[UserRepository],
        bot_user_repository: FromDishka[BotUserRepository],
    ) -> WebhookUsecase:
        return WebhookUsecase(
            bot_repository=bot_repository,
            user_repository=user_repository,
            bot_user_repository=bot_user_repository,
        )

    @provide(scope=Scope.APP)
    def get_active_bots_usecase(
        self,
        bot_repository: FromDishka[BotRepository],
    ) -> GetActiveBotsUsecase:
        return GetActiveBotsUsecase(bot_repository=bot_repository)
