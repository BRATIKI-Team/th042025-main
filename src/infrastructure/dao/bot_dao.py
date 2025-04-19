from piccolo.table import Table
from piccolo.columns import BigSerial, Varchar, ForeignKey, Integer, Text

from .user_dao import UserDAO


class BotDAO(Table):
    id: int = BigSerial(primary_key=True)
    user_id: int = ForeignKey(UserDAO)
    title: str = Varchar(length=255)
    description: str = Text()
    notification_period: int = Integer(length=1)
    token: str = Varchar(length=46)
