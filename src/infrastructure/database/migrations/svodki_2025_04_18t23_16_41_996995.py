from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Integer
from piccolo.columns.indexes import IndexMethod


ID = "2025-04-18T23:16:41:996995"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="svodki", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="BotDAO",
        tablename="bot_dao",
        column_name="notification_period",
        db_column_name="notification_period",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "length": 1,
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    return manager
