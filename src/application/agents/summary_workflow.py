from typing import List
import asyncio

from src.application.agents.parser.parser_agent import ParserAgent
from src.application.agents.sanitizer.sanitizer_agent import SanitizerAgent
from src.application.agents.summarizer.summarizer_agent import SummarizerAgent
from src.application.dto.summary_dto import SummaryDto
from src.application.services.index_service import IndexService
from src.domain.model.message_model import MessageModel


class SummaryWorkflow:
    def __init__(self, index_service: IndexService):
        self.__index_service = index_service

    async def start_workflow(
        self, bot_id: int, topic: str, messages: List[MessageModel]
    ) -> List[SummaryDto]:
        """
        Starts the summary workflow.

        Args:
            bot_id: The ID of the bot.
            topic: The topic of the messages.
            messages: The messages to summarize.

        Returns:
            Summaries ready to be sent to user.
        """
        parsed_messages = await self.__parse_messages(topic, messages)
        summaries = await self.__summarize_messages(parsed_messages)
        sanitized_summaries = await self.__sanitize_summaries(bot_id, summaries)

        if len(sanitized_summaries) > 0:
            # index summaries so we can exclude from future summaries the content that we
            # had already been sent to user
            await self.__index_service.index_summaries(bot_id, sanitized_summaries)

        # summaries_with_images = await self.__generate_images(sanitized_summaries)
        return sanitized_summaries

    async def __parse_messages(
        self, topic: str, messages: List[MessageModel]
    ) -> List[MessageModel]:
        """
        Extracts the appropriate messages by topic.

        Args:
            topic: The topic of the messages.
            messages: The messages to parse.

        Returns:
            The filtered messages.
        """
        parser_agent = ParserAgent(topic)
        return await parser_agent.execute(messages)

    async def __summarize_messages(
        self, messages: List[MessageModel]
    ) -> List[SummaryDto]:
        """
        Summarizes the messages, removing duplicates.

        Args:
            messages: The messages to summarize.

        Returns:
            The summarized messages.
        """
        summarizer_agent = SummarizerAgent()
        return await summarizer_agent.execute(messages)

    async def __sanitize_summaries(
        self, bot_id: int, summaries: List[SummaryDto]
    ) -> List[SummaryDto]:
        """
        Sanitizes the summaries, removing the information that had been already sent to user.
        This helps to avoid notifying same information multiple times.

        Args:
            bot_id: The ID of the bot.
            summaries: The summaries to sanitize.

        Returns:
            The sanitized summaries.
        """
        sanitizer_agent = SanitizerAgent(bot_id, summaries, self.__index_service)
        return await sanitizer_agent.execute()

    # async def __generate_images(self, summaries: List[SummaryDto]) -> List[SummaryExtendedDto]:
    #     """
    #     Generates images for the summaries. If metadata contains attachments, uses those instead of generating new images.

    #     Args:
    #         summaries: The summaries to generate images for.

    #     Returns:
    #         The summaries with images.
    #     """
    #     async def process_summary(summary: SummaryDto) -> SummaryExtendedDto:
    #         image_url = None

    #         # Check if metadata has attachments
    #         if summary.metadata and "attachments" in summary.metadata:
    #             return

    #         # Only generate image if no attachments were found
    #         if not image_url:
    #             image_generator = ImageGenerator()
    #             image_url = await image_generator.execute(summary.title)

    #         return SummaryExtendedDto(
    #             title=summary.title,
    #             content=summary.content,
    #             metadata=summary.metadata,
    #             image_url=image_url
    #         )

    #     # Process summaries in parallel
    #     tasks = [process_summary(summary) for summary in summaries]
    #     return await asyncio.gather(*tasks)
