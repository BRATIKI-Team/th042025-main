from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.domain.model.channel_info_model import ChannelInfoModel
from src.domain.model.channel_message_model import ChannelMessageModel


class TelegramRepository(ABC):
    @abstractmethod
    async def download_media(
        self, channel_username: str, message_id: int, file_name: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    async def get_messages(
        self,
        channel_username: str,
        limit: int = 10,
        offset_date: Optional[datetime] = None,
    ) -> List[ChannelMessageModel]:
        pass

    @abstractmethod
    async def get_channel_info(self, channel_username: str) -> ChannelInfoModel:
        pass
