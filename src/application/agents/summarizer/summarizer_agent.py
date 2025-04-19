from pydantic_ai import Agent
from typing import List

from pydantic_ai import Agent

from src.infrastructure.config import Config
from src.application.agents.summarizer import system_prompt

from src.application.dto.summary_response import SummaryResponse


class SummarizeAgent:
    def __init__(self):
        self.__llm_model_name = Config.OPENAI_MODEL_NAME
        self._agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Summirize scattered news, removing duplicates
        """
        return Agent(
            model=self.__llm_model_name,
            deps_type=List[str],
            output_type=List[SummaryResponse],
            system_prompt=system_prompt,
        )

    async def execute(self, deps: List[str]) -> List[SummaryResponse]:
        return await self._agent.run(" ".join(deps), deps=deps)
