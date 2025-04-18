from piccolo.conf.apps import AppConfig
from src.infrastructure.dao import table_classes
from src.infrastructure.config import config


APP_CONFIG = AppConfig(
    app_name="svodki",
    migrations_folder_path=config.MIGRATIONS_PATH,
    table_classes=table_classes,
    migration_dependencies=[],
    commands=[],
)
