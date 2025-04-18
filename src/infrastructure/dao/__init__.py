from src.infrastructure.dao.user_dao import UserDAO
from src.infrastructure.dao.bot_dao import BotDAO
from src.infrastructure.dao.source_dao import SourceDAO

table_classes: list = [
    UserDAO,
    BotDAO,
    SourceDAO,
]
