from dishka import AsyncContainer, Provider, make_async_container

from src.di.repository_container import RepositoryContainer
from src.di.services_container import ServicesContainer
from src.di.usecase_container import UsecaseContainer
from src.di.utils_container import UtilsContainer


def init_container(specific_providers: list[Provider] = []) -> AsyncContainer:
    return make_async_container(
        UtilsContainer(),
        RepositoryContainer(),
        UsecaseContainer(),
        ServicesContainer(),
        *specific_providers
    )
