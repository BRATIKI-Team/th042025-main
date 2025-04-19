from datetime import datetime
from typing import List, Optional

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.enum.bot_status_enum import BotStatus
from src.domain.model.bot_model import BotModel
from src.domain.model.pagination_model import PaginationModel
from src.domain.repository.bot_repository import BotRepository
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.value_object.bot_name_vo import BotNameVO
from src.domain.value_object.bot_token_vo import BotTokenVO
from src.infrastructure.dao.bot_dao import BotDAO


class BotRepositoryImpl(BotRepository):
    async def get_bot_by_token(self, token: str) -> Optional[BotModel]:
        dao = await BotDAO.objects().get(BotDAO.token == token).first()

        if dao is None:
            return None

        return BotDAO.from_dao(dao)

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
            status=BotStatus.ACTIVE.value,
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

        return BotDAO.from_dao(dao)

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

    async def get_my_bots(
        self, user_id: int, page: int, page_size: int
    ) -> PaginationModel[BotModel]:
        query: list[BotDAO] = (
            await BotDAO.objects()
            .where(BotDAO.user_id == user_id)
            .offset((page - 1) * page_size)
            .limit(page_size + 1)
        )

        models = [BotDAO.from_dao(dao) for dao in query]
        has_more = len(models) > page_size

        return PaginationModel(
            items=models[:page_size],
            has_more=has_more,
            page=page,
            page_size=page_size,
        )

    async def get_active_bots(self) -> List[BotModel]:
        daos = await BotDAO.objects().where(BotDAO.status == BotStatus.ACTIVE.value)

        return [BotDAO.from_dao(dao) for dao in daos]

    async def update_bot_status(self, bot_id: int, status: BotStatus) -> None:
        await BotDAO.update({BotDAO.status: status.value}).where(BotDAO.id == bot_id)

    async def delete_bot(self, bot_id: int) -> None:
        await BotDAO.delete().where(BotDAO.id == bot_id)
