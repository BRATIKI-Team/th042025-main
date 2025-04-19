from datetime import datetime
from typing import Optional

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.model.bot_model import BotModel
from src.domain.repository.bot_repository import BotRepository
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.value_object.bot_name_vo import BotNameVO
from src.domain.value_object.bot_token_vo import BotTokenVO
from src.infrastructure.dao.bot_dao import BotDAO


class BotRepositoryImpl(BotRepository):
    async def has_bot(self, user_id: int) -> bool:
        dao = await BotDAO.objects().get(BotDAO.user_id == user_id).first()

        return dao is not None

    async def create_bot(
        self,
        user_id: int,
        name: BotNameVO,
        description: BotDescriptionVO,
        period: BotNotificationPeriod,
        token: BotTokenVO,
    ) -> int:
        dao = await BotDAO.objects().create(
            user_id=user_id,
            title=name.value,
            description=description.value,
            token=token.value,
            notification_period=period.value,
        )

        return dao.id

    async def read_by_id(self, bot_id: int) -> Optional[BotModel]:
        """
        Get a bot by its ID.

        Args:
            bot_id: The ID of the bot to get

        Returns:
            BotModel: The bot model, or None if not found
        """
        dao = await BotDAO.objects().get(BotDAO.id == bot_id)

        if dao is None:
            return None

        return BotModel(
            id=dao.id,
            user_id=dao.user_id,
            title=BotNameVO(value=dao.title),
            description=BotDescriptionVO(value=dao.description),
            token=BotTokenVO(value=dao.token),
            notification_period=BotNotificationPeriod(dao.notification_period),
            last_notified_at=dao.last_notified_at,
        )

    async def update_last_notified_at(
        self, bot_id: int, last_notified_at: datetime
    ) -> None:
        """
        Update the last_notified_at timestamp for a bot.

        Args:
            bot_id: The ID of the bot to update
            last_notified_at: The new timestamp
        """
        await BotDAO.update({BotDAO.last_notified_at: last_notified_at}).where(
            BotDAO.id == bot_id
        )
