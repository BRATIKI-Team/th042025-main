from piccolo.table import Table
from piccolo.columns import BigSerial, ForeignKey

from src.infrastructure.dao.source_dao import SourceDAO
from src.infrastructure.dao.bot_dao import BotDAO


class SourceBotDAO(Table):
    """
    DAO для связи между источниками и ботами.
    Эта таблица хранит информацию о том, какие боты связаны с какими источниками.
    """
    id: int = BigSerial(primary_key=True)
    source_id: int = ForeignKey(SourceDAO)
    bot_id: int = ForeignKey(BotDAO) 