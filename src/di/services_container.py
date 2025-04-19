

from dishka import Provider, Scope, provide

from src.application.services.index_service import IndexService
from src.domain.repository.chroma_repository import ChromaRepository


class ServicesContainer(Provider):
    @provide(scope=Scope.APP)
    def index_service(
        self, chroma_repository: ChromaRepository
    ) -> IndexService:
        return IndexService(chroma_repository)
