from pydantic_ai import Agent
from pydantic_ai.models import Model

from src.application.agents.topic_validator.system_prompt import system_prompt


class TopicValidatorAgent:
    def __init__(
        self,
        llm: Model
    ):
        self.__llm = llm
        self.__agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Create an agent for validating topic titles.
        """
        return Agent(
            model=self.__llm,
            tools=[],  # No external tools needed for validation
            deps_type=str,
            output_type=bool,
            system_prompt=system_prompt
        )

    async def execute(self, topic: str) -> bool:
        """
        Execute the agent to validate the topic title.

        Returns:
            bool: True if the topic is valid and suitable for notification collection,
                  False otherwise.
        """
        result = await self.__agent.run(topic)
        return result.output
