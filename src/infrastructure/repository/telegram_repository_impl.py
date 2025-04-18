import asyncio
from datetime import datetime
import logging
import os
from typing import List, Optional
from telethon.tl.types import Message as TelethonMessage, Channel as TelethonChannel
from telethon.errors import FloodWaitError, ChatAdminRequiredError, ChannelPrivateError

from src.domain.exception.telegram_error import TelegramError
from src.domain.model.channel_attachment_model import ChannelAttachmentModel
from src.domain.model.channel_info_model import ChannelInfoModel
from src.domain.model.channel_message_model import ChannelMessageModel
from src.domain.repository.telegram_repository import TelegramRepository
from src.infrastructure.tg.telegram_client import TelegramClient


class TelegramRepositoryImpl(TelegramRepository):
    def __init__(
        self, tg_client: TelegramClient, download_path: str, max_workers: int = 10
    ) -> None:
        self._tg_client = tg_client
        self._download_path = download_path
        self._semaphore = asyncio.Semaphore(value=max_workers)

    async def download_media(
        self, channel_username: str, message_id: int, file_name: Optional[str] = None
    ) -> None:
        """
        Download a media file from a message

        Args:
            channel_username (str): Channel username or ID
            message_id (int): ID of the message containing the media
            file_name (Optional[str]): Custom file name for the downloaded file

        Returns:
            str: Path to the downloaded file

        Raises:
            TelegramError: If download fails
        """
        try:
            # Create downloads directory if it doesn't exist
            os.makedirs(self._download_path, exist_ok=True)

            # Get the message
            async with self._tg_client:
                message = await self._tg_client.engine.get_messages(
                    channel_username, ids=message_id
                )

            if not message:
                raise TelegramError(
                    f"Message with ID {message_id} not found in channel {channel_username}"
                )

            if not message.media:
                raise TelegramError(f"Message {message_id} does not contain any media")

            # Generate file path
            if not file_name:
                if hasattr(message.media, "document") and hasattr(
                    message.media.document, "attributes"
                ):
                    for attr in message.media.document.attributes:
                        if hasattr(attr, "file_name"):
                            file_name = attr.file_name
                            break
                if not file_name:
                    file_name = f"file_{message_id}"

            file_path = os.path.join(self._download_path, file_name)

            # Download the file
            try:
                downloaded_path = await self._tg_client.engine.download_media(
                    message.media, file=file_path
                )
            except Exception as e:
                logging.error(f"Failed to download media: {str(e)}")
                raise TelegramError(f"Failed to download media: {str(e)}")

            if not downloaded_path:
                raise TelegramError(
                    f"Failed to download file from message {message_id}"
                )

            logging.info(
                f"Successfully downloaded file from message {message_id} to {downloaded_path}"
            )
        except Exception as e:
            logging.error(
                f"Failed to download file from message {message_id}: {str(e)}"
            )

            raise TelegramError(f"File download failed: {str(e)}")

    async def get_messages(
        self,
        channel_username: str,
        limit: int = 10,
        offset_date: Optional[datetime] = None,
    ) -> List[ChannelMessageModel]:
        """
        Get messages from a channel

        Args:
            channel_username (str): Channel username or ID
            limit (int): Maximum number of messages to retrieve
            offset_date (Optional[datetime]): Start date for message retrieval

        Returns:
            List[ChannelMessageModel]: List of messages

        Raises:
            TelegramError: If message retrieval fails
        """
        async with self._semaphore:
            try:
                messages_dict = {}  # Dictionary to store messages by their ID
                grouped_messages: dict[
                    str, list[ChannelMessageModel]
                ] = {}  # Dictionary to store grouped messages

                async with self._tg_client:
                    async for message in self._tg_client.engine.iter_messages(
                        channel_username, limit=limit, offset_date=offset_date
                    ):
                        if isinstance(message, TelethonMessage):
                            # Get channel_id from peer_id if it's a channel message
                            source = None
                            if hasattr(message, "peer_id") and hasattr(
                                message.peer_id, "channel_id"
                            ):
                                source = str(message.peer_id.channel_id)

                            # Check if message is part of a group
                            grouped_id = getattr(message, "grouped_id", None)

                            if grouped_id:
                                # If this is a grouped message, add it to the group
                                if grouped_id not in grouped_messages:
                                    grouped_messages[grouped_id] = []
                                grouped_messages[grouped_id].append(message)
                            else:
                                # If this is a standalone message, create it
                                messages_dict[message.id] = ChannelMessageModel(
                                    message_id=message.id,
                                    date=message.date,
                                    text=message.text or "",
                                    attachments=[],
                                    source=source,
                                )

                                # Add attachments if present
                                if message.media:
                                    attachments = await self._get_message_attachments(
                                        message
                                    )
                                    messages_dict[message.id].attachments.extend(
                                        attachments
                                    )

                # Process grouped messages
                for _, group in grouped_messages.items():
                    # Sort messages in group by ID
                    group.sort(key=lambda x: x.id)

                    # Create main message from the first message in group
                    main_message = group[0]
                    main_msg = ChannelMessageModel(
                        message_id=main_message.id,
                        date=main_message.date,
                        text=main_message.text or "",
                        attachments=[],
                        source=str(main_message.peer_id.channel_id)
                        if hasattr(main_message.peer_id, "channel_id")
                        else None,
                    )

                    # Add attachments from all messages in group
                    for msg in group:
                        if msg.media:
                            attachments = await self._get_message_attachments(msg)
                            main_msg.attachments.extend(attachments)

                    messages_dict[main_message.id] = main_msg

                # Convert dictionary to list and sort by message_id in descending order
                messages = list(messages_dict.values())
                messages.sort(key=lambda x: x.message_id, reverse=True)
                return messages

            except FloodWaitError as e:
                logging.warning(f"Rate limit hit, waiting {e.seconds} seconds")
                raise TelegramError(f"Rate limit exceeded: {str(e)}")
            except (ChatAdminRequiredError, ChannelPrivateError) as e:
                logging.error(f"Access error: {str(e)}")
                raise TelegramError(f"Access denied: {str(e)}")
            except Exception as e:
                logging.error(f"Failed to get messages: {str(e)}")
                raise TelegramError(f"Message retrieval failed: {str(e)}")

    async def _get_message_attachments(
        self, message: TelethonMessage
    ) -> List[ChannelAttachmentModel]:
        """
        Extract attachments from a Telegram message

        Args:
            message (TelethonMessage): Telegram message object

        Returns:
            List[ChannelAttachmentModel]: List of extracted attachments
        """
        attachments = []
        if message.media:
            try:
                if hasattr(message.media, "photo"):
                    photo = message.media.photo
                    if hasattr(photo, "id"):
                        attachments.append(
                            ChannelAttachmentModel(
                                type="photo",
                                file_id=str(photo.id),
                                mime_type="image/jpeg",
                            )
                        )
                elif hasattr(message.media, "document"):
                    doc = message.media.document
                    if hasattr(doc, "id"):
                        file_name = ""
                        if hasattr(doc, "attributes"):
                            for attr in doc.attributes:
                                if hasattr(attr, "file_name"):
                                    file_name = attr.file_name
                                    break

                        if not file_name:
                            file_name = f"document_{doc.id}"

                        attachments.append(
                            ChannelAttachmentModel(
                                type="document",
                                file_id=str(doc.id),
                                file_name=file_name,
                                mime_type=doc.mime_type,
                                size=doc.size,
                            )
                        )
            except Exception as e:
                logging.warning(f"Failed to process attachment: {str(e)}")

        return attachments

    async def get_channel_info(self, channel_username: str) -> ChannelInfoModel:
        """
        Get information about a channel

        Args:
            channel_username (str): Channel username or ID

        Returns:
            ChannelInfoModel: Channel information

        Raises:
            TelegramError: If channel info retrieval fails
        """
        async with self._semaphore:
            try:
                async with self._tg_client:
                    entity = await self._tg_client.engine.get_entity(channel_username)

                    if not isinstance(entity, TelethonChannel):
                        raise TelegramError(
                            f"Entity {channel_username} is not a channel"
                        )

                    full_channel = await self._tg_client.engine.get_entity(entity)

                # Safely get channel attributes
                channel_id = getattr(entity, "id", None)
                title = getattr(entity, "title", "")
                username = getattr(entity, "username", None)
                description = getattr(full_channel, "about", None)
                participants_count = getattr(full_channel, "participants_count", None)
                is_verified = getattr(entity, "verified", False)

                # Get photo URL if available
                photo_url = None

                if hasattr(entity, "photo"):
                    photo_url = await self._get_channel_photo_url(entity)

                return ChannelInfoModel(
                    id=channel_id,
                    title=title,
                    username=username,
                    description=description,
                    photo_url=photo_url,
                    participants_count=participants_count,
                    is_verified=is_verified,
                )
            except Exception as e:
                logging.error(f"Failed to get channel info: {str(e)}")
                raise TelegramError(f"Channel info retrieval failed: {str(e)}")

    async def _get_channel_photo_url(self, entity: TelethonChannel) -> Optional[str]:
        """
        Get channel photo URL

        Args:
            entity (TelethonChannel): Channel entity

        Returns:
            Optional[str]: Base64 encoded photo URL or None if no photo
        """
        if hasattr(entity, "photo") and entity.photo:
            try:
                async with self._tg_client:
                    photo = await self._tg_client.engine.download_profile_photo(
                        entity, file=bytes
                    )

                if photo:
                    return f"data:image/jpeg;base64,{photo.hex()}"
            except Exception as e:
                logging.warning(f"Failed to get channel photo: {str(e)}")

        return None
