from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.model.pagination_model import PaginationModel
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.model.bot_model import BotModel
from src.domain.value_object.bot_name_vo import BotNameVO
from src.domain.value_object.bot_token_vo import BotTokenVO


class BotRepository(ABC):
    @abstractmethod
    async def has_bot(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_bot_by_token(self, token: str) -> Optional[BotModel]:
        pass

    @abstractmethod
    async def create_bot(
        self,
        user_id: int,
        name: BotNameVO,
        description: BotDescriptionVO,
        period: BotNotificationPeriod,
        token: BotTokenVO,
    ) -> int:
        """Create bot and return its id"""

    @abstractmethod
    async def read_by_id(self, bot_id: int) -> Optional[BotModel]:
        """
        Get a bot by its ID.

        Args:
            bot_id: The ID of the bot to get

        Returns:
            BotModel: The bot model, or None if not found
        """

    @abstractmethod
    async def update_last_notified_at(
        self, bot_id: int, last_notified_at: datetime
    ) -> None:
        """
        Update the last_notified_at timestamp for a bot.

        Args:
            bot_id: The ID of the bot to update
            last_notified_at: The new timestamp
        """

    @abstractmethod
    async def get_my_bots(
        self, user_id: int, page: int, page_size: int
    ) -> PaginationModel[BotModel]:
        pass

    @abstractmethod
    async def get_active_bots(self) -> List[BotModel]:
        pass
