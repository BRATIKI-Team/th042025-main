from typing import List

from src.application.dto.summary_dto import SummaryDto
from src.domain.repository.summary_repository import SummaryRepository
from src.infrastructure.dao.summary_dao import SummaryDAO


class SummaryRepositoryImpl(SummaryRepository):
    async def create_many(self, bot_id: int, summaries: List[SummaryDto]) -> List[int]:
        """
        Create multiple summaries in the database.

        Args:
            bot_id: The ID of the bot that owns these summaries
            summaries: List of summaries to create

        Returns:
            List of created summary IDs
        """
        # Create a list of SummaryDAO objects
        query = SummaryDAO.insert()
        for summary in summaries:
            query.add(SummaryDAO(
                bot_id=bot_id,
                title=summary.title,
                summary=summary.content,
                metadata=summary.metadata,
            ))


        # Insert all summaries in a single operation
        created_daos = await query

        # Return the IDs of the created summaries
        return [dao['id'] for dao in created_daos]