from piccolo.table import Table
from piccolo.columns import BigSerial, Varchar, ForeignKey, Integer, Text, Timestamp

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.enum.bot_status_enum import BotStatus
from src.domain.model.bot_model import BotModel
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.value_object.bot_name_vo import BotNameVO
from src.domain.value_object.bot_token_vo import BotTokenVO

from .user_dao import UserDAO


class BotDAO(Table):
    id: BigSerial = BigSerial(primary_key=True)
    user_id: ForeignKey = ForeignKey(UserDAO)
    title: Varchar = Varchar(length=255)
    description: Text = Text()
    notification_period: Integer = Integer(length=1)
    token: Varchar = Varchar(length=46)
    last_notified_at: Timestamp = Timestamp(null=True, default=None)
    status: Integer = Integer(length=1)

    @staticmethod
    def from_dao(dao: "BotDAO") -> BotModel:
        return BotModel(
            id=dao.id,
            user_id=dao.user_id,
            title=BotNameVO(value=dao.title),
            description=BotDescriptionVO(value=dao.description),
            token=BotTokenVO(value=dao.token),
            notification_period=BotNotificationPeriod(dao.notification_period),
            last_notified_at=dao.last_notified_at,
            status=BotStatus(dao.status),
        )
