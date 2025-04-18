from abc import ABC, abstractmethod

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.value_object.bot_name_vo import BotNameVO


class BotRepository(ABC):
    @abstractmethod
    async def has_bot(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def create_bot(
        self, user_id: int, name: BotNameVO, period: BotNotificationPeriod
    ) -> int:
        """Create bot and return its id"""
