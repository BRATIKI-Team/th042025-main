from dishka import Provider, Scope, provide

from src.domain.repository.bot_repository import BotRepository
from src.infrastructure.repository.bot_repository_impl import BotRepositoryImpl


class RepositoryContainer(Provider):
    @provide(scope=Scope.APP)
    def bot_repository(self) -> BotRepository:
        return BotRepositoryImpl()
