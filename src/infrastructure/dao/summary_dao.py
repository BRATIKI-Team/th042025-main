from piccolo.table import Table
from piccolo.columns import BigSerial, ForeignKey, Text, Varchar

from .bot_dao import BotDAO

class SummaryDAO(Table):
    id: int = BigSerial(primary_key=True)
    bot_id: int = ForeignKey(BotDAO)
    title: str = Varchar(length=255)
    summary: str = Text()