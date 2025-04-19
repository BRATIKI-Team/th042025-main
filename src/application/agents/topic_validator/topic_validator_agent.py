from pydantic_ai import Agent

from src.infrastructure.config import Config
from src.application.agents.topic_validator import system_prompt


class TopicValidatorAgent:
    def __init__(
        self,
    ):
        self.__llm_model_name = Config.OPENAI_MODEL_NAME
        self.__agent = self.__create_agent()

    def __create_agent(self) -> Agent:
        """
        Create an agent for validating topic titles.
        """
        return Agent(
            model=self.__llm_model_name,
            tools=[],  # No external tools needed for validation
            deps_type=str,
            output_type=bool,
            system_prompt=system_prompt
        )

    async def execute(self, topic) -> bool:
        """
        Execute the agent to validate the topic title.

        Returns:
            bool: True if the topic is valid and suitable for notification collection,
                  False otherwise.
        """
        result = await self.__agent.run(topic)
        return result.output
