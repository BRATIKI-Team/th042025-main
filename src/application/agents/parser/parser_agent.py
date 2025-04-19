
import json
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from src.infrastructure.config import Config
from src.application.agents.parser import system_prompt


# TODO: use MessageDao when will be ready
class Message(BaseModel):
    content: str = Field(..., description="The text content of the message")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the message (e.g., timestamp, author, etc.)"
    )

class ParserAgent:
    def __init__(
        self,
        topic: str,
        messages: List[Message]
    ):
        self.__llm_model_name = Config.OPENAI_MODEL_NAME
        self.__topic = topic
        self.__messages = messages
        self.__agent = self.__create_agent()


    def __create_agent(self) -> Agent:
        system_prompt_formatted = system_prompt.replace("{{topic}}", self.__topic)
        return Agent(
            model=self.__llm_model_name,
            tools=[],
            deps_type=str,
            output_type=List[Message],
            system_prompt=system_prompt_formatted
        )


    async def execute(self) -> List[Message]:
        messages_json = json.dumps([message.model_dump() for message in self.__messages])

        result = await self.__agent.run(messages_json)
        return result.output
