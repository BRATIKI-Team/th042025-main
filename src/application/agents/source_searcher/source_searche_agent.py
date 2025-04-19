from typing import List
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from openai import OpenAI

from src.application.dto.source_generate_response import SourceGenerateResponse
from src.infrastructure.config import Config
from src.application.agents.source_searcher import system_prompt

class SourceSearcherAgent:
    def __init__(
        self,
        topic: str
    ):
        self.__topic = topic
        self.__llm_model_name = Config.OPENAI_MODEL_NAME
        self.__agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Create an agent for searching for Telegram channels using DuckDuckGo.
        """
        tools = [duckduckgo_search_tool]
        return Agent(
            model=self.__llm_model_name,
            tools=tools,
            deps_type=str,
            output_type=List[SourceGenerateResponse],
            system_prompt=system_prompt,
            retries=10 # Up to 10 retries because of the rate limit
        )
    
    async def execute(self) -> List[SourceGenerateResponse]:
        """
        Execute the agent to search for Telegram channels.
        """
        result = await self.__agent.run(self.__topic)
        return result.output
            
