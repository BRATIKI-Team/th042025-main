from typing import List
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import QueryEngineTool
from llama_index.core.llms import OpenAI

from src.application.services import IndexService
from src.infrastructure.config import Config
from src.infrastructure.dao.summary_dao import SummaryDAO
from src.application.agents.sanytizer import system_prompt


class SanytizerAgent:
    def __init__(
        self,
        bot_id: str,
        summaries_to_sanitize: List[SummaryDAO],
        index_service: IndexService
    ):
        self.__bot_id = bot_id
        self.__summaries_to_sanitize = summaries_to_sanitize
        self.__index_service = index_service
        self.__llm = OpenAI(api_key=Config.OPENAI_API_KEY, model=Config.OPENAI_MODEL_NAME)
        self.__agent = self.__create_agent()


    def __create_agent(self) -> FunctionAgent:
        tools = [self.__create_query_engine_tool(summary) for summary in self.__summaries_to_sanitize]
        return FunctionAgent.from_tools(
            system_prompt=system_prompt,
            tools=tools,
            llm=self.__llm,
            verbose=True
        )


    def __create_query_engine_tool(self, summary: SummaryDAO) -> QueryEngineTool:
        index = self.__index_service.get_index(self.__bot_id)
        query_engine = index.as_query_engine()
        return QueryEngineTool.from_defaults(
            query_engine=query_engine,
            description=f"Provides information about possible existing summaries in db about - {summary.title}."
        )


    async def execute(self) -> List[SummaryDAO]:
        """
        Sanitizes the summaries of a bot.

        Args:
            bot_id: The ID of the bot to sanitize the summaries of.
            summaries_to_sanitize: The summaries to sanitize.

        Returns:
            The sanitized summaries.
        """
        summaries = "\n".join(
            f"Summary {i + 1}:\n"
            f"Title: {summary.title}\n"
            f"Content: {summary.summary}\n"
            for i, summary in enumerate(self.__summaries_to_sanitize)
        )

        result = await self.__agent.run(summaries)
        print(str(result))
        

    
