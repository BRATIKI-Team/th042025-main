from dishka import FromDishka, Provider, Scope, provide
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models import Model

from src.application.agents.source_searcher import SourceSearcherAgent
from src.application.agents.topic_validator.topic_validator_agent import (
    TopicValidatorAgent,
)
from src.infrastructure.config import config
from src.infrastructure.tg.telegram_client import TelegramClient
from src.infrastructure.tg.telegram_client_factory import TelegramClientFactory


class UtilsContainer(Provider):
    @provide(scope=Scope.APP)
    async def telegram_client(
        self, factory: FromDishka[TelegramClientFactory]
    ) -> TelegramClient:
        """
        Provides a TelegramClient instance through the factory.
        The factory ensures we have a single, connected client instance.
        """
        return await factory.get_client()

    @provide(scope=Scope.APP)
    def telegram_client_factory(self) -> TelegramClientFactory:
        """
        Provides the TelegramClientFactory singleton instance.
        """
        return TelegramClientFactory()

    @provide(scope=Scope.APP)
    def provide_openai_model(self) -> Model:
        return OpenAIModel(
            model_name=config.OPENAI_MODEL_NAME,
            provider=OpenAIProvider(api_key=config.OPENAI_API_KEY.get_secret_value()),
        )

    @provide(scope=Scope.APP)
    def provide_validate_topic_agent(
        self, llm: FromDishka[Model]
    ) -> TopicValidatorAgent:
        return TopicValidatorAgent(llm=llm)

    @provide(scope=Scope.APP)
    def provide_source_searcher_agent(
        self,
        llm: FromDishka[Model],
    ) -> SourceSearcherAgent:
        return SourceSearcherAgent(llm=llm)
