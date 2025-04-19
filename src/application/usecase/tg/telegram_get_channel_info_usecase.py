from src.domain.model.channel_info_model import ChannelInfoModel
from src.domain.repository.telegram_repository import TelegramRepository


class TelegramGetChannelInfoUsecase:
    def __init__(self, repository: TelegramRepository) -> None:
        self._repository = repository

    async def execute(self, channel_username: str) -> ChannelInfoModel:
        return await self._repository.get_channel_info(
            channel_username=channel_username
        )
