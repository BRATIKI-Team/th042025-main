import chromadb
from piccolo.engine import SQLiteEngine
from piccolo.conf.apps import AppRegistry
from src.infrastructure.config import config

DB = SQLiteEngine(path=config.DATABASE_PATH)
CHROMA_DB = chromadb.PersistentClient(path=config.CHROMADB_PATH)

APP_REGISTRY = AppRegistry(apps=["src.infrastructure.database.piccolo_app"])
