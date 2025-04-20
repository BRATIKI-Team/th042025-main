from typing import List
import logging

from src.domain.model.grouped_source_model import GroupedSourceModel
from src.domain.model.message_model import MessageModel
from src.domain.repository.source_repository import SourceRepository
from src.domain.repository.message_repository import MessageRepository
from src.domain.repository.telegram_repository import TelegramRepository


logger = logging.getLogger(__name__)


class GetSourceMessagesUsecase:
    def __init__(
        self,
        source_repository: SourceRepository,
        message_repository: MessageRepository,
        telegram_repository: TelegramRepository,
    ):
        self._source_repository = source_repository
        self._message_repository = message_repository
        self._telegram_repository = telegram_repository

    async def execute(self, grouped_source: GroupedSourceModel) -> List[MessageModel]:
        """
        Get messages from the specified source group based on the source type.
        """
        logger.info(
            f"Getting messages for source group: {grouped_source.url} (type: {grouped_source.type})"
        )

        # Get messages based on source type
        messages = []
        if grouped_source.type == 0:  # Telegram source
            messages = await self._get_telegram_messages(grouped_source)
        else:
            logger.warning(f"Unsupported source type: {grouped_source.type}")

        # Update last_hit_datetime for all source IDs
        source_ids = [source.id for source in grouped_source.sources]
        await self._source_repository.update_last_hit_datetime(source_ids)

        return messages

    async def _get_telegram_messages(
        self, grouped_source: GroupedSourceModel
    ) -> List[MessageModel]:
        """
        Get messages from a Telegram source.
        """
        # Extract channel username from URL
        # Assuming URL format is https://t.me/channelname or https://telegram.me/channelname
        channel_username = self._extract_telegram_channel_username(grouped_source.url)

        if not channel_username:
            logger.error(f"Invalid Telegram URL: {grouped_source.url}")
            return []

        try:
            # Get messages from Telegram
            telegram_messages = await self._telegram_repository.get_messages(
                channel_username=channel_username,
                limit=10,  # Adjust as needed
                offset_date=grouped_source.last_hit_datetime,
            )

            if not telegram_messages:
                return []

            # Collect all external_ids to check existence in a single query
            external_ids = {str(msg.message_id) for msg in telegram_messages}

            # Check which messages already exist in the database
            existing_external_ids = (
                await self._message_repository.exists_by_external_ids(external_ids)
            )

            # Filter out messages that already exist
            new_messages = [
                msg
                for msg in telegram_messages
                if str(msg.message_id) not in existing_external_ids
            ]

            if not new_messages:
                return []

            # Prepare messages for bulk insert
            messages_to_create = []

            for msg in new_messages:
                # Create message content
                content = msg.text

                # Add attachment information to content if needed
                if msg.attachments:
                    attachment_info = []
                    for attachment in msg.attachments:
                        if attachment.type == "photo":
                            attachment_info.append(f"[Photo: {attachment.file_id}]")
                        elif attachment.type == "document":
                            attachment_info.append(
                                f"[Document: {attachment.file_name or 'unnamed'}]"
                            )
                        else:
                            attachment_info.append(f"[{attachment.type}]")

                    if attachment_info:
                        content += "\n\nAttachments: " + ", ".join(attachment_info)

                # Create metadata
                metadata = {
                    "message_id": msg.message_id,
                    "date": msg.date.isoformat(),
                    "source": msg.source,
                    "attachments": [
                        {
                            "channel_username": attachment.channel_username,
                            "message_id": attachment.message_id,
                            "type": attachment.type,
                            "file_id": attachment.file_id,
                            "file_name": attachment.file_name,
                            "mime_type": attachment.mime_type,
                            "size": attachment.size,
                        }
                        for attachment in msg.attachments
                    ],
                }

                # Add a message entry for each source in the group
                for source in grouped_source.sources:
                    messages_to_create.append(
                        {
                            "source_id": source.id,
                            "content": content,
                            "external_id": str(msg.message_id),
                            "metadata": metadata,
                            "published_at": msg.date,
                        }
                    )

            # Create all messages in a single database operation
            return await self._message_repository.create_many(messages_to_create)

        except Exception as e:
            logger.error(f"Error getting Telegram messages: {str(e)}")
            return []

    def _extract_telegram_channel_username(self, url: str) -> str:
        """
        Extract channel username from Telegram URL.
        """
        # Handle different URL formats
        if "t.me/" in url:
            parts = url.split("t.me/")
            if len(parts) > 1:
                return parts[1].strip("/")

        if "telegram.me/" in url:
            parts = url.split("telegram.me/")
            if len(parts) > 1:
                return parts[1].strip("/")
        if "@" in url:
            parts = url.split("@")
            if len(parts) > 1:
                return parts[1].strip("@")

        return ""
