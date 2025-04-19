from datetime import datetime
from typing import Optional

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.enum.bot_status_enum import BotStatus
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.value_object.bot_name_vo import BotNameVO
from src.domain.value_object.bot_token_vo import BotTokenVO


class BotModel:
    """
    Model representing a bot.
    """

    def __init__(
        self,
        id: int,
        user_id: int,
        title: BotNameVO,
        description: BotDescriptionVO,
        notification_period: BotNotificationPeriod,
        token: BotTokenVO,
        status: BotStatus,
        last_notified_at: Optional[datetime] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.token = token
        self.description = description
        self.notification_period = notification_period
        self.last_notified_at = last_notified_at
        self.status = status
