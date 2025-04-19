from chromadb import Collection
from llama_index.vector_stores.chroma import ChromaVectorStore
from src.infrastructure.database.engine import CHROMA_DB
from src.infrastructure.repository import ChromaRepository


class ChromaRepositoryImp(ChromaRepository):
    def __init__(self):
        self.__db = CHROMA_DB

    def get_or_create_vector_store(self, collection_name: str) -> ChromaVectorStore:
        """
        Retrieves a vector store for a given collection name. If the collection does not exist, it will be created.

        Args:
        - collection_name: The name of the collection to retrieve or create

        Returns:
        """
        collection = self._get_or_create_collection(collection_name)
        print(f"found collection by name {collection_name}", collection)

        return ChromaVectorStore(collection)
    
    def drop_collection_if_exists(self, collection_name: str) -> None:
        """
        Drops a collection if it exists.

        Args:
        - collection_name: The name of the collection to drop
        """
        try:
            self.__db.delete_collection(collection_name)
        except Exception as e:
            print(f"Error dropping collection {collection_name}: {e}")

    def _get_or_create_collection(self, name: str) -> Collection:
        """
        Retrieves a collection by name. If the collection does not exist, it will be created.

        Args:
        - name: The name of the collection to retrieve or create
        """
        return self.__db.get_or_create_collection(name)
