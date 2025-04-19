from piccolo.table import Table
from piccolo.columns import BigSerial, ForeignKey, Text, Varchar, JSON

from .bot_dao import BotDAO


class SummaryDAO(Table):
    id: BigSerial = BigSerial(primary_key=True)
    bot_id: ForeignKey = ForeignKey(BotDAO)
    title: Varchar = Varchar(length=255)
    summary: Text = Text()
    metadata: JSON = JSON()
