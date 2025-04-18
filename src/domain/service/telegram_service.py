from datetime import datetime
from typing import List, Optional
from src.domain.model.channel_info_model import ChannelInfoModel
from src.domain.model.channel_message_model import ChannelMessageModel
from src.domain.repository.telegram_repository import TelegramRepository


class TelegramService:
    def __init__(self, repository: TelegramRepository) -> None:
        self._repository = repository

    async def get_messages(
        self,
        channel_username: str,
        limit: int = 10,
        offset_date: Optional[datetime] = None,
    ) -> List[ChannelMessageModel]:
        return await self._repository.get_messages(channel_username, limit, offset_date)

    async def get_channel_info(self, channel_username: str) -> ChannelInfoModel:
        return await self._repository.get_channel_info(channel_username)

    async def download_media(
        self, channel_username: str, message_id: int, file_name: Optional[str] = None
    ) -> None:
        return await self._repository.download_media(
            channel_username, message_id, file_name
        )
