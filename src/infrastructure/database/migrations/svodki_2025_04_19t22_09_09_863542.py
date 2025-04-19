from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import BigSerial
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import JSON
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.timestamp import TimestampNow
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


class SourceDAO(Table, tablename="source_dao", schema=None):
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


ID = "2025-04-19T22:09:09:863542"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="svodki", description=DESCRIPTION
    )

    manager.add_table(
        class_name="MessageDAO",
        tablename="message_dao",
        schema=None,
        columns=None,
    )

    manager.add_table(
        class_name="SourceDAO", tablename="source_dao", schema=None, columns=None
    )

    manager.add_table(
        class_name="BotDAO", tablename="bot_dao", schema=None, columns=None
    )

    manager.add_table(
        class_name="BotUserDAO",
        tablename="bot_user_dao",
        schema=None,
        columns=None,
    )

    manager.add_table(
        class_name="UserDAO", tablename="user_dao", schema=None, columns=None
    )

    manager.add_column(
        table_class_name="MessageDAO",
        tablename="message_dao",
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
        table_class_name="MessageDAO",
        tablename="message_dao",
        column_name="source_id",
        db_column_name="source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": SourceDAO,
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
        table_class_name="MessageDAO",
        tablename="message_dao",
        column_name="content",
        db_column_name="content",
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
        table_class_name="MessageDAO",
        tablename="message_dao",
        column_name="external_id",
        db_column_name="external_id",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
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
        table_class_name="MessageDAO",
        tablename="message_dao",
        column_name="created_at",
        db_column_name="created_at",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
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
        table_class_name="MessageDAO",
        tablename="message_dao",
        column_name="published_at",
        db_column_name="published_at",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": None,
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
        table_class_name="MessageDAO",
        tablename="message_dao",
        column_name="metadata",
        db_column_name="metadata",
        column_class_name="JSON",
        column_class=JSON,
        params={
            "default": "{}",
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
        table_class_name="SourceDAO",
        tablename="source_dao",
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
        table_class_name="SourceDAO",
        tablename="source_dao",
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
        table_class_name="SourceDAO",
        tablename="source_dao",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
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
        table_class_name="SourceDAO",
        tablename="source_dao",
        column_name="url",
        db_column_name="url",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
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
        table_class_name="SourceDAO",
        tablename="source_dao",
        column_name="description",
        db_column_name="description",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
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
        table_class_name="SourceDAO",
        tablename="source_dao",
        column_name="type",
        db_column_name="type",
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

    manager.add_column(
        table_class_name="SourceDAO",
        tablename="source_dao",
        column_name="status",
        db_column_name="status",
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

    manager.add_column(
        table_class_name="SourceDAO",
        tablename="source_dao",
        column_name="last_hit_datetime",
        db_column_name="last_hit_datetime",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": None,
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
        table_class_name="BotDAO",
        tablename="bot_dao",
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
        table_class_name="BotDAO",
        tablename="bot_dao",
        column_name="title",
        db_column_name="title",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
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
            "unique": True,
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
        column_name="last_notified_at",
        db_column_name="last_notified_at",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": None,
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
        column_name="status",
        db_column_name="status",
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
        table_class_name="UserDAO",
        tablename="user_dao",
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

    return manager
