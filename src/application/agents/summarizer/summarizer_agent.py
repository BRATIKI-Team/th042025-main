from pydantic_ai import Agent
from typing import List

from pydantic_ai import Agent

from src.domain.model.message_model import MessageModel
from src.infrastructure.config import config
from src.application.agents.summarizer import system_prompt
from src.application.dto.summary_dto import SummaryDto

class SummarizerAgent:
    def __init__(self):
        self.__llm_model_name = config.OPENAI_MODEL_NAME
        self._agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Create an agent for summarizing scattered news, removing duplicates
        """
        print("---**Summarizer Agent** | creating | ....", end="\n\n")
        return Agent(
            model=self.__llm_model_name,
            deps_type=List[str],
            output_type=List[SummaryDto],
            system_prompt=system_prompt,
        )

    async def execute(self, messages: List[MessageModel]) -> List[SummaryDto]:
        """
        Execute the summarizer agent.
        """
        print("---**Summarizer Agent** | executing | ....", end="\n\n")
        messages_json = [message.model_dump() for message in messages]

        print(f"---**Summarizer Agent** | input | => {messages_json}", end="\n\n")
        result = await self._agent.run(messages_json)

        print(f"---**Summarizer Agent** | output | => {result.output}", end="\n\n")
        return result.output
