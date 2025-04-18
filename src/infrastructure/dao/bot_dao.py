from piccolo.table import Table
from piccolo.columns import BigSerial, Varchar, ForeignKey, Integer

from .user_dao import UserDAO


class BotDAO(Table):
    id: int = BigSerial(primary_key=True)
    user_id: int = ForeignKey(UserDAO)
    title: str = Varchar(length=255)
    notification_period: int = Integer(length=1)
