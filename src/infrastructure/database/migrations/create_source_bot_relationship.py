from piccolo.migrations import MigrationManager
from piccolo.columns import BigSerial, ForeignKey, IndexMethod


async def forwards():
    manager = MigrationManager()
    
    # Создаем таблицу source_bot_dao
    manager.create_table(
        table_class_name="SourceBotDAO",
        tablename="source_bot_dao",
        schema=None,
    )
    
    # Добавляем колонку id
    manager.add_column(
        table_class_name="SourceBotDAO",
        tablename="source_bot_dao",
        column_name="id",
        db_column_name="id",
        column_class_name="BigSerial",
        column_class=BigSerial,
        params={
            "primary_key": True,
            "null": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )
    
    # Добавляем колонку source_id
    manager.add_column(
        table_class_name="SourceBotDAO",
        tablename="source_bot_dao",
        column_name="source_id",
        db_column_name="source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": "source_dao",
            "on_delete": "CASCADE",
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
    
    # Добавляем колонку bot_id
    manager.add_column(
        table_class_name="SourceBotDAO",
        tablename="source_bot_dao",
        column_name="bot_id",
        db_column_name="bot_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": "bot_dao",
            "on_delete": "CASCADE",
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
    
    # Добавляем уникальное ограничение на source_id и bot_id
    manager.add_constraint(
        table_class_name="SourceBotDAO",
        tablename="source_bot_dao",
        constraint_name="unique_source_bot",
        constraint_type="unique",
        columns=["source_id", "bot_id"],
        schema=None,
    )
    
    return manager


async def backwards():
    manager = MigrationManager()
    
    # Удаляем таблицу source_bot_dao
    manager.drop_table(
        table_class_name="SourceBotDAO",
        tablename="source_bot_dao",
        schema=None,
    )
    
    return manager 