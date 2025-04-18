from dishka import Provider, Scope, provide

from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.source_repository import SourceRepository
from src.infrastructure.repository.bot_repository_impl import BotRepositoryImpl
from src.infrastructure.repository.source_repository_impl import SourceRepositoryImpl


class RepositoryContainer(Provider):
    @provide(scope=Scope.APP)
    def bot_repository(self) -> BotRepository:
        return BotRepositoryImpl()

    @provide(scope=Scope.APP)
    def source_repository(self) -> SourceRepository:
        return SourceRepositoryImpl()
