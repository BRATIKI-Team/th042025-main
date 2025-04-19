import json
from typing import List, Dict, Any, Set
from datetime import datetime

from src.domain.model.message_model import MessageModel
from src.domain.repository.message_repository import MessageRepository
from src.infrastructure.dao.message_dao import MessageDAO


class MessageRepositoryImpl(MessageRepository):
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
        # If published_at is not provided, try to extract it from metadata
        if published_at is None and "date" in metadata:
            try:
                published_at = datetime.fromisoformat(metadata["date"])
            except (ValueError, TypeError):
                pass
        
        message_dao = await MessageDAO.insert(
            MessageDAO(
                source_id=source_id,
                content=content,
                external_id=external_id,
                created_at=datetime.now(),
                published_at=published_at,
                metadata=metadata
            )
        ).execute()
        
        return MessageModel(
            id=message_dao.id,
            source_id=message_dao.source_id,
            content=message_dao.content,
            external_id=message_dao.external_id,
            created_at=message_dao.created_at,
            published_at=message_dao.published_at,
            metadata=message_dao.metadata
        )
    
    async def read_by_source_id(self, source_id: int) -> List[MessageModel]:
        """
        Get all messages for a specific source.
        """
        messages = await MessageDAO.select().where(MessageDAO.source_id == source_id).execute()
        
        return [
            MessageModel(
                id=message.id,
                source_id=message.source_id,
                content=message.content,
                external_id=message.external_id,
                created_at=message.created_at,
                published_at=message.published_at,
                metadata=message.metadata
            )
            for message in messages
        ]
    
    async def exists_by_external_id(self, external_id: str) -> bool:
        """
        Check if a message with the given external_id already exists.
        """
        message = await MessageDAO.objects().get(MessageDAO.external_id == external_id).first()
        
        return message is not None
    
    async def exists_by_external_ids(self, external_ids: Set[str]) -> Set[str]:
        """
        Check which of the given external_ids already exist in the database.
        Returns a set of external_ids that already exist.
        """
        if not external_ids:
            return set()
        
        # Используем правильный синтаксис для IN запроса в Piccolo
        existing_messages = await MessageDAO.select(MessageDAO.external_id).where(
            MessageDAO.external_id.is_in(list(external_ids))
        )
        
        # Extract external_ids from the result
        return {message['external_id'] for message in existing_messages}
    
    async def create_many(
        self,
        messages: List[Dict[str, Any]]
    ) -> List[MessageModel]:
        """
        Create multiple messages in the database in a single operation.
        Returns the created message models.
        """
        if not messages:
            return []
        
        query = MessageDAO.insert()
        
        # Prepare DAO objects for bulk insert
        for msg in messages:
            # Extract published_at from metadata if not provided
            published_at = msg.get("published_at")
            if published_at is None and "date" in msg["metadata"]:
                try:
                    published_at = datetime.fromisoformat(msg["metadata"]["date"])
                except (ValueError, TypeError):
                    pass
            
            query.add(
                MessageDAO(
                    source_id=msg["source_id"],
                    content=msg["content"],
                    external_id=msg["external_id"],
                    created_at=datetime.now(),
                    published_at=published_at,
                    metadata=msg["metadata"]
                )
            )
        
        # Perform bulk insert
        inserted_daos = await query.returning(*MessageDAO.all_columns())

        # Convert to models
        return [
            MessageDAO.from_dao(MessageDAO.from_dict({
                **dao,
                "metadata": json.loads(dao.get("metadata", "{}"))
            }))
            for dao in inserted_daos
        ]