from piccolo.table import Table
from piccolo.columns import BigSerial, ForeignKey

from .user_dao import UserDAO
from .bot_dao import BotDAO


class BotUserDAO(Table):
    id: BigSerial = BigSerial(primary_key=True)
    user_id: ForeignKey = ForeignKey(UserDAO)
    bot_id: ForeignKey = ForeignKey(BotDAO)
