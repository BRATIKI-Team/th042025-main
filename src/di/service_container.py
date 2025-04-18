from dishka import FromDishka, Provider

from src.domain.repository.telegram_repository import TelegramRepository
from src.domain.service.telegram_service import TelegramService


class ServiceContainer(Provider):
    def telegram_service(
        self, repository: FromDishka[TelegramRepository]
    ) -> TelegramService:
        return TelegramService(repository=repository)
