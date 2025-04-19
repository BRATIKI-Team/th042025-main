import json
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from src.domain.model.message_model import MessageModel
from src.infrastructure.config import Config
from src.application.agents.parser import system_prompt



class ParserAgent:
    def __init__(self, topic: str):
        self.__llm_model_name = Config.OPENAI_MODEL_NAME
        self.__topic = topic
        self.__agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        system_prompt_formatted = system_prompt.replace("{{topic}}", self.__topic)
        return Agent(
            model=self.__llm_model_name,
            tools=[],
            deps_type=str,
            output_type=List[MessageModel],
            system_prompt=system_prompt_formatted,
        )

    async def execute(self, messages: List[MessageModel]) -> List[MessageModel]:
        messages_json = json.dumps(
            [message.model_dump() for message in messages]
        )

        result = await self.__agent.run(messages_json)
        return result.output
