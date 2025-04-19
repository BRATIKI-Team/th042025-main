from typing import List
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.models import Model

from src.application.dto.source_generate_response import SourceGenerateResponse
from src.application.agents.source_searcher.prompts import system_prompt
from src.application.agents.source_searcher.tools import validate_channel_tool
from src.domain.repository.telegram_repository import TelegramRepository


class SourceSearcherAgent:
    def __init__(self, llm: Model, telegram_repository: TelegramRepository):
        self.__llm = llm
        self.__telegram_repository = telegram_repository
        self.__agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Создает агента для поиска Telegram каналов с использованием DuckDuckGo и валидации каналов.
        """
        tools = [
            duckduckgo_search_tool(),
            validate_channel_tool(self.__telegram_repository)
        ]
        return Agent(
            model=self.__llm,
            tools=tools,
            deps_type=str,
            output_type=List[SourceGenerateResponse],
            system_prompt=system_prompt,
            retries=10,  # До 10 попыток из-за ограничения скорости
        )

    async def execute(self, topic: str) -> List[SourceGenerateResponse]:
        """
        Выполняет агента для поиска Telegram каналов.
        """
        result = await self.__agent.run(topic)
        return result.output
