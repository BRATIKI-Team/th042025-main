from llama_index.vector_stores.chroma import ChromaVectorStore
from abc import ABC, abstractmethod


class ChromaRepository(ABC):
    @abstractmethod
    def get_or_create_vector_store(self, collection_name: str) -> ChromaVectorStore:
        pass

    @abstractmethod
    async def drop_collection_if_exists(self, collection_name: str) -> None:
        pass
