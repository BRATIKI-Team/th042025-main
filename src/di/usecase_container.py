from dishka import FromDishka, Provider, Scope, provide

from src.application.usecase.get_pending_source_usecase import GetPendingSourceUsecase
from src.application.usecase.has_bot_usecase import HasBotUsecase
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.source_repository import SourceRepository


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
