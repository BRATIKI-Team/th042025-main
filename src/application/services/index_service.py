from typing import List
from llama_index.core import StorageContext, VectorStoreIndex, Document

from src.domain.repository.chroma_repository import ChromaRepository
from src.infrastructure.dao.summary_dao import SummaryDAO


class IndexService:
    def __init__(self, chroma_repository: ChromaRepository) -> None:
        self.__chroma_repository = chroma_repository

    async def index_summaries(
        self, bot_id: str, summaries: List[SummaryDAO]
    ) -> VectorStoreIndex:
        """
        Creates an index for a received summaries.

        Args:
        - bot_id: Unique identifier for the bot
        - summaries: List of SummaryDAO objects containing the summaries

        Returns:
        A VectorStoreIndex object representing the created index for the summaries
        """

        documents = [
            Document(text=summary.summary, metadata={"title": summary.title})
            for summary in summaries
        ]

        return await self.__index(bot_id, documents)

    def get_index(self, bot_id: str) -> VectorStoreIndex:
        """
        Retrieves an existing index for querying purposes.

        Args:
        - chat_id: Unique identifier for the chat session

        Returns:
        A VectorStoreIndex object for the specified chat_id
        """
        collection_name = self.__get_collection_name(bot_id)
        vector_store = self.__chroma_repository.get_or_create_vector_store(collection_name)

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return VectorStoreIndex.from_vector_store(
            vector_store=vector_store, storage_context=storage_context
        )

    async def __index(self, bot_id: str, documents: List[Document]) -> VectorStoreIndex:
        """
        Creates an index for a received documents. If an index already exists for the given chat_id,
        it will be dropped and recreated.

        Args:
        - chat_id: Unique identifier for the chat session
        - attachment: Attachment object containing the file data and metadata

        Returns:
        A VectorStoreIndex object representing the created index for the document
        """
        collection_name = self.__get_collection_name(bot_id)
        await self.__chroma_repository.drop_collection_if_exists(collection_name)

        vector_store = self.__chroma_repository.get_or_create_vector_store(collection_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return VectorStoreIndex.from_documents(documents, storage_context)
    
    @staticmethod
    def __get_collection_name(bot_id: str) -> str:
        return f"bot_collection_{bot_id}"
