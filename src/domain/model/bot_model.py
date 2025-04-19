from datetime import datetime
from typing import Optional

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod


class BotModel:
    """
    Model representing a bot.
    """
    
    def __init__(
        self,
        id: int,
        user_id: int,
        title: str,
        notification_period: int,
        last_notified_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.notification_period = notification_period
        self.last_notified_at = last_notified_at
    
    @property
    def notification_period_enum(self) -> BotNotificationPeriod:
        """
        Get the notification period as an enum.
        
        Returns:
            BotNotificationPeriod: The notification period enum
        """
        return BotNotificationPeriod(self.notification_period) 