from piccolo.table import Table
from piccolo.columns import BigSerial, Varchar, ForeignKey, Integer, Text, Timestamp

from .user_dao import UserDAO


class BotDAO(Table):
    id: BigSerial = BigSerial(primary_key=True)
    user_id: ForeignKey = ForeignKey(UserDAO)
    title: Varchar = Varchar(length=255)
    description: Text = Text()
    notification_period: Integer = Integer(length=1)
    token: Varchar = Varchar(length=46)
    last_notified_at: Timestamp = Timestamp(null=True, default=None)
