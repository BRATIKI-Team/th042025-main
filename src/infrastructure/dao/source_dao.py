from piccolo.table import Table
from piccolo.columns import BigSerial, Varchar, Integer, ForeignKey, Timestamp
from datetime import datetime

from src.domain.enum.source_status_enum import SourceStatus
from src.domain.model.source_model import SourceModel
from src.infrastructure.dao.bot_dao import BotDAO


class SourceDAO(Table):
    id: int = BigSerial(primary_key=True)
    bot_id: int = ForeignKey(BotDAO)
    name: str = Varchar(length=255)
    url: str = Varchar(length=255)
    description: str = Varchar(length=255)
    type: int = Integer(length=1)
    status: int = Integer(length=1)
    last_hit_datetime: datetime = Timestamp(null=True, default=None)

    @staticmethod
    def from_dao(dao: "SourceDAO") -> SourceModel:
        return SourceModel(
            id=dao.id,
            name=dao.name,
            status=SourceStatus(dao.status),
            url=dao.url,
            description=dao.description,
            type=dao.type,
            last_hit_datetime=dao.last_hit_datetime,
        )
