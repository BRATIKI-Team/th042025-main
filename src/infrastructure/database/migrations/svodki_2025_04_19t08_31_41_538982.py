from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import BigSerial
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Varchar
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class BotDAO(Table, tablename="bot_dao", schema=None):
    id = BigSerial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name=None,
        secret=False,
    )


class UserDAO(Table, tablename="user_dao", schema=None):
    id = BigSerial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name=None,
        secret=False,
    )


ID = "2025-04-19T08:31:41:538982"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="svodki", description=DESCRIPTION
    )

    manager.add_table(
        class_name="BotUserDAO",
        tablename="bot_user_dao",
        schema=None,
        columns=None,
    )

    manager.add_column(
        table_class_name="BotUserDAO",
        tablename="bot_user_dao",
        column_name="id",
        db_column_name="id",
        column_class_name="BigSerial",
        column_class=BigSerial,
        params={
            "null": False,
            "primary_key": True,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="BotUserDAO",
        tablename="bot_user_dao",
        column_name="user_id",
        db_column_name="user_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": UserDAO,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
            "null": True,
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

    manager.add_column(
        table_class_name="BotUserDAO",
        tablename="bot_user_dao",
        column_name="bot_id",
        db_column_name="bot_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": BotDAO,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
            "null": True,
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

    manager.add_column(
        table_class_name="BotDAO",
        tablename="bot_dao",
        column_name="description",
        db_column_name="description",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
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

    manager.add_column(
        table_class_name="BotDAO",
        tablename="bot_dao",
        column_name="token",
        db_column_name="token",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 46,
            "default": "",
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
