from datetime import datetime
from typing import List, Optional
from src.domain.model.channel_message_model import ChannelMessageModel
from src.domain.repository.telegram_repository import TelegramRepository


class TelegramGetMessagesUsecase:
    def __init__(self, repository: TelegramRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        channel_username: str,
        limit: int = 10,
        offset_date: Optional[datetime] = None,
    ) -> List[ChannelMessageModel]:
        return await self._repository.get_messages(
            channel_username=channel_username, limit=limit, offset_date=offset_date
        )
