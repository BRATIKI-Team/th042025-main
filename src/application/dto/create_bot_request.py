from pydantic import BaseModel

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.value_object.bot_name_vo import BotNameVO


class CreateBotRequest(BaseModel):
    user_id: int
    name: BotNameVO
    notification_period: BotNotificationPeriod
