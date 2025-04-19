from abc import ABC, abstractmethod
from typing import List, Dict, Any, Set, Optional
from datetime import datetime

from src.domain.model.message_model import MessageModel


class MessageRepository(ABC):
    @abstractmethod
    async def create(
            self,
            source_id: int,
            content: str,
            external_id: str,
            metadata: Dict[str, Any],
            published_at: datetime | None = None
    ) -> MessageModel:
        """
        Create a new message in the database.
        Returns the created message model.
        """
        pass

    @abstractmethod
    async def read_by_source_id(self, source_id: int) -> List[MessageModel]:
        """
        Get all messages for a specific source.
        """
        pass

    @abstractmethod
    async def exists_by_external_id(self, external_id: str) -> bool:
        """
        Check if a message with the given external_id already exists.
        """
        pass

    @abstractmethod
    async def exists_by_external_ids(self, external_ids: Set[str]) -> Set[str]:
        """
        Check which of the given external_ids already exist in the database.
        Returns a set of external_ids that already exist.
        """
        pass

    @abstractmethod
    async def create_many(
            self,
            messages: List[Dict[str, Any]]
    ) -> List[MessageModel]:
        """
        Create multiple messages in the database in a single operation.
        Returns the created message models.

        Each message in the list should be a dictionary with the following keys:
        - source_id: int
        - content: str
        - external_id: str
        - metadata: Dict[str, Any]
        - published_at: datetime | None
        """
        pass

    @abstractmethod
    async def read_by_bot_and_filter_by_created(
            self,
            bot_id: int,
            min_created_at: Optional[datetime] = None
    ) -> List[MessageModel]:
        """
       Retrieve all messages as MessageModel instances for sources associated with the specified bot_id,
       optionally filtered by creation date if min_created_at is provided.

       Args:
           bot_id: The ID of the bot whose sources' messages are to be retrieved.
           min_created_at: Optional minimum creation date for messages (if None, no date filter is applied).

       Returns:
           List[MessageModel]: A list of MessageModel objects.
       """
        pass
