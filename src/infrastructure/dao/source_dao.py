from piccolo.table import Table
from piccolo.columns import BigSerial, Varchar, Integer, ForeignKey, Timestamp

from src.domain.enum.source_status_enum import SourceStatus
from src.domain.model.source_model import SourceModel
from src.infrastructure.dao.bot_dao import BotDAO


class SourceDAO(Table):
    id: BigSerial = BigSerial(primary_key=True)
    bot_id: ForeignKey = ForeignKey(BotDAO)
    name: Varchar = Varchar(length=255)
    url: Varchar = Varchar(length=255)
    description: Varchar = Varchar(length=255)
    type: Integer = Integer(length=1)
    status: Integer = Integer(length=1)
    last_hit_datetime: Timestamp = Timestamp(null=True, default=None)

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
