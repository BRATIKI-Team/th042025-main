from piccolo.table import Table
from piccolo.columns import BigSerial, Varchar, ForeignKey

from .user_dao import UserDAO


class BotDAO(Table):
    id: int = BigSerial(primary_key=True)
    user_id: int = ForeignKey(UserDAO)
    title: str = Varchar(length=255)
