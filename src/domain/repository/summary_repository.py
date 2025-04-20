from abc import ABC, abstractmethod
from typing import List

from src.application.dto.summary_dto import SummaryDto


class SummaryRepository(ABC):
    @abstractmethod
    async def create_many(self, bot_id: int, summaries: List[SummaryDto]) -> List[int]:
        """
        Create multiple summaries in the database.

        Args:
            bot_id: The ID of the bot that owns these summaries
            summaries: List of summaries to create

        Returns:
            List of created summary IDs
        """
        pass 