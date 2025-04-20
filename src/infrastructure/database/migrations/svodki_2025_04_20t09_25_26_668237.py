from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Time
from piccolo.columns.defaults.time import TimeNow
from piccolo.columns.indexes import IndexMethod


ID = "2025-04-20T09:25:26:668237"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="svodki", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="SummaryDAO",
        tablename="summary_dao",
        column_name="created_at",
        db_column_name="created_at",
        column_class_name="Time",
        column_class=Time,
        params={
            "default": TimeNow(),
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
