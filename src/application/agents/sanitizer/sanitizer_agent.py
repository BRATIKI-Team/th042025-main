from typing import List
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import QueryEngineTool
from llama_index.llms.openai import OpenAI
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
import json

from src.application.dto.summary_dto import SummaryDto
from src.application.services import IndexService
from src.application.agents.sanitizer import system_prompt
from src.infrastructure.config import Config


class SanitizerAgent:
    def __init__(
        self,
        bot_id: int,
        summaries_to_sanitize: List[SummaryDto],
        index_service: IndexService,
    ):
        self.__bot_id = bot_id
        self.__summaries_to_sanitize = summaries_to_sanitize
        self.__index_service = index_service
        self.__llm = OpenAI(api_key=Config.OPENAI_API_KEY, model=Config.OPENAI_MODEL_NAME)
        self.__agent = self.__create_agent()

    def __create_agent(self) -> FunctionAgent:
        """
        Create an agent for sanitizing summaries.
        """
        tools = [
            self.__create_query_engine_tool(summary)
            for summary in self.__summaries_to_sanitize
        ]
        return FunctionAgent(
            system_prompt=system_prompt, tools=tools, llm=self.__llm, verbose=True
        )

    def __create_query_engine_tool(self, summary: SummaryDto) -> QueryEngineTool:
        """
        Create a query engine tool for a summary.
        """
        index = self.__index_service.get_index(str(self.__bot_id))

        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=5,
            verbose=True
        )
        
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)]
        )

        return QueryEngineTool.from_defaults(
            query_engine=query_engine,
            description=f"Provides information about possible existing summaries in db about - {summary.title}.",
        )

    async def execute(self) -> List[SummaryDto]:
        """
        Sanitizes the summaries of a bot.

        Args:
            bot_id: The ID of the bot to sanitize the summaries of.
            summaries_to_sanitize: The summaries to sanitize.

        Returns:
            The sanitized summaries as a list of SummaryDto objects.
        """
        summaries_json = json.dumps([summary.model_dump() for summary in self.__summaries_to_sanitize]) 

        result = await self.__agent.run(summaries_json)

        try:
            # Parse the JSON response
            sanitized_summaries = json.loads(str(result))

            # Convert JSON objects to SummaryDto objects
            return [
                SummaryDto(
                    title=summary["title"],
                    content=summary["content"],
                    metadata=summary["metadata"]
                )

                for summary in sanitized_summaries
            ]
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse agent response as JSON: {str(e)}")
        except KeyError as e:
            raise ValueError(
                f"Invalid JSON structure in agent response: missing required field {str(e)}"
            )
