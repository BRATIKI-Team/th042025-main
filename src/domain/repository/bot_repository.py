from abc import ABC, abstractmethod

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.value_object.bot_name_vo import BotNameVO
from src.domain.value_object.bot_token_vo import BotTokenVO


class BotRepository(ABC):
    @abstractmethod
    async def has_bot(self, user_id: int) -> bool:
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
