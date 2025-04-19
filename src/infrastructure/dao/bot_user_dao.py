from piccolo.table import Table
from piccolo.columns import BigSerial, ForeignKey

from .user_dao import UserDAO
from .bot_dao import BotDAO


class BotUserDAO(Table):
    id: int = BigSerial(primary_key=True)
    user_id: int = ForeignKey(UserDAO)
    bot_id: int = ForeignKey(BotDAO)
