import json
from typing import List
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from src.domain.model.message_model import MessageModel
from src.infrastructure.config import config
from .prompts import system_prompt



class ParserAgent:
    def __init__(self, topic: str):
        self.__topic = topic
        self.__llm = OpenAIModel(
            model_name=config.OPENAI_MODEL_NAME,
            provider=OpenAIProvider(api_key=config.OPENAI_API_KEY.get_secret_value())
        )
        self.__agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Create an agent for parsing messages.
        """
        print(f"---**Parser Agent** | creating | topic | => {self.__topic}", end="\n\n")
        system_prompt_formatted = system_prompt.replace("{{topic}}", self.__topic)

        print(f"---**Parser Agent** | system_prompt | => {system_prompt_formatted}", end="\n\n")
        return Agent(
            model=self.__llm,
            tools=[],
            deps_type=str,
            output_type=List[MessageModel],
            system_prompt=system_prompt_formatted,
        )

    async def execute(self, messages: List[MessageModel]) -> List[MessageModel]:
        """
        Execute the parser agent.
        """
        print("---**Parser Agent** | executing | ....", end="\n\n")
        messages_json = json.dumps(
            [message.model_dump() for message in messages]
        )

        print(f"---**Parser Agent** | input | => {messages_json}", end="\n\n")
        result = await self.__agent.run(messages_json)

        print(f"---**Parser Agent** | output | => {result.output}", end="\n\n")
        return result.output
