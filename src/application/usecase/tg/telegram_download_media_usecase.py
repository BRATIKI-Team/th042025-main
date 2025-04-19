from typing import Optional
from src.domain.repository.telegram_repository import TelegramRepository


class TelegramDownloadMediaUsecase:
    def __init__(self, repository: TelegramRepository) -> None:
        self._repository = repository

    async def execute(
        self, channel_username: str, message_id: int, file_name: Optional[str] = None
    ) -> None:
        await self._repository.download_media(
            channel_username=channel_username,
            message_id=message_id,
            file_name=file_name,
        )
