from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Time
from piccolo.columns.defaults.time import TimeNow

from src.infrastructure.dao.summary_dao import SummaryDAO


ID = "2025-04-20T12:01:52:027335"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="svodki", description=DESCRIPTION
    )

    manager.drop_column(
        table_class_name="SummaryDAO",
        tablename="summary_dao",
        column_name="created_at",
        db_column_name="created_at",
        schema=None,
    )

    return manager
