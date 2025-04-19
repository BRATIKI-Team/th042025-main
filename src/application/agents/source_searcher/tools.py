from typing import Optional
from pydantic_ai import Tool

from src.domain.repository.telegram_repository import TelegramRepository
from src.domain.exception.telegram_error import TelegramError


def validate_channel_tool(telegram_repository: TelegramRepository) -> Tool:
    """
    Создает инструмент для валидации существования Telegram канала.
    
    Args:
        telegram_repository: Репозиторий для работы с Telegram
        
    Returns:
        Tool: Инструмент для валидации канала
    """
    async def validate_channel(channel_url: str) -> bool:
        """
        Проверяет существование Telegram канала.
        
        Args:
            channel_url: URL канала в формате @channelname
            
        Returns:
            bool: True если канал существует, False в противном случае
        """
        try:
            # Убираем @ из начала URL если он есть
            channel_username = channel_url.lstrip('@')
            await telegram_repository.get_channel_info(channel_username)
            return True
        except TelegramError:
            return False

    return Tool(
        name="validateChannel",
        description="Проверяет существование Telegram канала по его URL",
        function=validate_channel,
        input_type=str,
        output_type=bool
    ) 