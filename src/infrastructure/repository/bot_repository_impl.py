from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.repository.bot_repository import BotRepository
from src.domain.value_object.bot_name_vo import BotNameVO
from src.infrastructure.dao.bot_dao import BotDAO


class BotRepositoryImpl(BotRepository):
    async def has_bot(self, user_id: int) -> bool:
        dao = await BotDAO.objects().get(BotDAO.user_id == user_id).first()

        return dao is not None

    async def create_bot(
        self, user_id: int, name: BotNameVO, period: BotNotificationPeriod
    ) -> int:
        dao = await BotDAO.objects().create(
            user_id=user_id,
            title=name.value,
            period=period.value,
        )

        return dao.id
