from dishka import FromDishka, Provider, Scope, provide

from src.application.usecase.has_bot_usecase import HasBotUsecase
from src.domain.repository.bot_repository import BotRepository


class UsecaseContainer(Provider):
    @provide(scope=Scope.APP)
    def has_bot_usecase(
        self, bot_repository: FromDishka[BotRepository]
    ) -> HasBotUsecase:
        return HasBotUsecase(bot_repository=bot_repository)
