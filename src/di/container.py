from dishka import AsyncContainer, Provider, make_async_container


def init_container(specific_providers: list[Provider] = []) -> AsyncContainer:
    return make_async_container(*specific_providers)
