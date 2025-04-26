import json
from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from openai import RateLimitError

from typing import List

from src.domain.model.message_model import MessageModel
from src.infrastructure.config import config
from src.application.dto.summary_dto import SummaryDto
from src.infrastructure.utils.backoff import backoff
from .prompts import system_prompt


class SummarizerAgent:
    def __init__(self):
        self.__llm = OpenAIModel(
            model_name=config.OPENAI_MODEL_NAME,
            provider=OpenAIProvider(api_key=config.OPENAI_API_KEY.get_secret_value()),
        )
        self._agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Create an agent for summarizing scattered news, removing duplicates
        """
        print("---**Summarizer Agent** | creating | ....", end="\n\n")
        return Agent(
            model=self.__llm,
            deps_type=List[str],
            output_type=List[SummaryDto],
            system_prompt=system_prompt,
        )

    @backoff(
        exception=RateLimitError,
        max_tries=5,
        max_time=60,
        initial_delay=1.0,
        exponential_base=2.0,
    )
    async def execute(self, messages: List[MessageModel]) -> List[SummaryDto]:
        """
        Execute the summarizer agent.
        """

        def datetime_handler(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(
                f"Object of type {type(obj).__name__} is not JSON serializable"
            )

        print("---**Summarizer Agent** | executing | ....", end="\n\n")
        messages_json = json.dumps(
            [message.model_dump() for message in messages], default=datetime_handler
        )

        print(f"---**Summarizer Agent** | input | => {messages_json}", end="\n\n")
        result = await self._agent.run(messages_json)

        print(f"---**Summarizer Agent** | output | => {result.output}", end="\n\n")
        return result.output
