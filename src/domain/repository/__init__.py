from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.source_repository import SourceRepository
from src.domain.repository.chroma_repository import ChromaRepository
import re


def convert_title_to_vector_index(title: str) -> str:
    """
    Convert a title into vector index format.
    Example: "Title for something!?" -> "vector_index_title_for_something"
    """
    # Remove all special characters except letters, numbers and spaces
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    # Convert to lowercase and replace spaces with underscores
    normalized = cleaned.lower().replace(" ", "_")
    # Add prefix and return
    return f"vector_index_{normalized}"


__all__ = [
    "BotRepository",
    "SourceRepository",
    "ChromaRepository",
]
