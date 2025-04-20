from datetime import datetime
from typing import Dict, List

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
            query = query.add(
                SummaryDAO(
                    bot_id=bot_id,
                    title=summary.title,
                    summary=summary.content,
                    metadata=summary.metadata,
                    created_at=datetime.now(),
                )
            )

        # Insert all summaries in a single operation
        created_daos = await query

        # Return the IDs of the created summaries
        return [dao["id"] for dao in created_daos]

    async def get_metrics(self, bot_id: int) -> Dict[datetime, int]:
        """
        Get metrics for a bot.
        """
        daos = await SummaryDAO.objects().where(SummaryDAO.bot_id == bot_id)

        metrics: dict[str, int] = {}
        for summary in daos:
            metrics[summary.created_at] = metrics.get(summary.created_at, 0) + 1
        return metrics
