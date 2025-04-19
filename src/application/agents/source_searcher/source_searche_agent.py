from typing import List
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.models import Model

from src.application.dto.source_generate_response import SourceGenerateResponse
from src.application.agents.source_searcher import system_prompt


class SourceSearcherAgent:
    def __init__(self, llm: Model):
        self.__llm = llm
        self.__agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Create an agent for searching for Telegram channels using DuckDuckGo.
        """
        tools = [duckduckgo_search_tool]
        return Agent(
            model=self.__llm,
            tools=tools,
            deps_type=str,
            output_type=List[SourceGenerateResponse],
            system_prompt=system_prompt,
            retries=10,  # Up to 10 retries because of the rate limit
        )

    async def execute(self, topic: str) -> List[SourceGenerateResponse]:
        """
        Execute the agent to search for Telegram channels.
        """
        result = await self.__agent.run(topic)
        return result.output
