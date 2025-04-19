from piccolo.table import Table
from piccolo.columns import BigSerial, Varchar, ForeignKey, Timestamp, JSON, Text

from src.infrastructure.dao.source_dao import SourceDAO
from src.domain.model.message_model import MessageModel


class MessageDAO(Table):
    id: BigSerial = BigSerial(primary_key=True)
    source_id: ForeignKey = ForeignKey(SourceDAO)
    content: Text = Text()
    external_id: Varchar = Varchar(length=255)
    created_at: Timestamp = Timestamp()
    published_at: Timestamp = Timestamp(null=True, default=None)
    metadata: JSON = JSON()

    @staticmethod
    def from_dao(dao: "MessageDAO") -> MessageModel:
        """
        Convert a MessageDAO instance to a MessageModel.

        Args:
            dao: The MessageDAO instance to convert

        Returns:
            MessageModel: The converted model
        """
        return MessageModel(
            id=dao.id,
            source_id=dao.source_id,
            content=dao.content,
            external_id=dao.external_id,
            created_at=dao.created_at,
            published_at=dao.published_at,
            metadata=dao.metadata,
        )
