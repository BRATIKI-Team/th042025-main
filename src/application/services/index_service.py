from typing import List
from llama_index.core import StorageContext, VectorStoreIndex, Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import TextNode

from src.domain.repository.chroma_repository import ChromaRepository
from src.infrastructure.dao.summary_dao import SummaryDAO
from src.infrastructure.config import config


class IndexService:
    def __init__(self, chroma_repository: ChromaRepository) -> None:
        self.__chroma_repository = chroma_repository
        self.__embed_model = OpenAIEmbedding(
            api_key=config.OPENAI_API_KEY.get_secret_value()
        )

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
        nodes = []

        for summary in summaries:
            text = f"{summary.title}\n\n{summary.content}"

            metadata = {"title": summary.title}
            metadata.update(summary.metadata)

            text_node = TextNode(text=text, metadata=metadata)
            nodes.append(text_node)

        collection_name = self.__get_collection_name(bot_id)
        if (await self.__chroma_repository.collection_exists(collection_name)):
            return await self.__update_index(bot_id, nodes)
        
        return await self.__index(bot_id, nodes)


    def get_index(self, bot_id: str) -> VectorStoreIndex:
        """
        Retrieves an existing index for querying purposes.

        Args:
        - chat_id: Unique identifier for the chat session

        Returns:
        A VectorStoreIndex object for the specified chat_id
        """
        collection_name = self.__get_collection_name(bot_id)
        vector_store = self.__chroma_repository.get_or_create_vector_store(
            collection_name
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context,
            embed_model=self.__embed_model,
        )


    async def __index(self, collection_name: str, nodes: List[TextNode]) -> VectorStoreIndex:
        """
        Creates an index for a received documents. If an index already exists for the given chat_id,
        it will be dropped and recreated.

        Args:
        - chat_id: Unique identifier for the chat session
        - attachment: Attachment object containing the file data and metadata

        Returns:
        A VectorStoreIndex object representing the created index for the document
        """
        await self.__chroma_repository.drop_collection_if_exists(collection_name)

        vector_store = self.__chroma_repository.get_or_create_vector_store(
            collection_name
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return VectorStoreIndex(
            nodes, storage_context=storage_context, embed_model=self.__embed_model
        )
    

    async def __update_index(self, collection_name: str, nodes: List[TextNode]) -> VectorStoreIndex:
        vector_store = self.__chroma_repository.get_or_create_vector_store(
            collection_name
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context,
            embed_model=self.__embed_model,
        )

        index.insert_nodes(nodes)
        return index


    @staticmethod
    def __get_collection_name(bot_id: str) -> str:
        return f"bot_collection_{bot_id}"
