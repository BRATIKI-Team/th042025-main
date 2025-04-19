from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar


ID = "2025-04-19T18:23:11:080207"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="svodki", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="BotDAO",
        tablename="bot_dao",
        column_name="token",
        db_column_name="token",
        params={"unique": True},
        old_params={"unique": False},
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    return manager
