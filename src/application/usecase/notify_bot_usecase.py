from typing import List
import logging
import os
import asyncio
from datetime import datetime

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import (
    InputFile,
    FSInputFile,
    InputMediaPhoto,
    InputMediaDocument,
    InputMediaVideo,
)

from src.application.agents.summary_workflow import SummaryWorkflow
from src.application.services import IndexService
from src.domain.model.message_model import MessageModel
from src.domain.repository.bot_repository import BotRepository
from src.domain.repository.message_repository import MessageRepository
from src.domain.repository.summary_repository import SummaryRepository
from src.domain.repository.user_bot_repository import UserBotRepository
from src.domain.repository.telegram_repository import TelegramRepository
from src.infrastructure.config import config


logger = logging.getLogger(__name__)


class NotifyBotUsecase:
    """
    Usecase for notifying a bot about new messages.
    """

    # Семафор для предотвращения гонок при одновременном вызове
    _semaphore = asyncio.Semaphore(1)
    _semaphore_timeout = 300  # 5 минут таймаут
    _active_tasks = set()  # Множество активных задач

    def __init__(
        self,
        bot_repository: BotRepository,
        user_bot_repository: UserBotRepository,
        message_repository: MessageRepository,
        summary_repository: SummaryRepository,
        telegram_repository: TelegramRepository,
        index_service: IndexService,
    ):
        self._bot_repository = bot_repository
        self._user_bot_repository = user_bot_repository
        self._message_repository = message_repository
        self._summary_repository = summary_repository
        self._telegram_repository = telegram_repository
        self._workflow = SummaryWorkflow(index_service=index_service)

    async def execute(self, bot_id: int) -> None:
        """
        Execute the usecase.

        Args:
            bot_id: The ID of the bot to notify
            messages: The messages to notify about
        """
        task_id = id(asyncio.current_task())
        self._active_tasks.add(task_id)
        logger.info(f"Starting notification for bot {bot_id} (task {task_id}, active tasks: {len(self._active_tasks)})")

        try:
            # Пытаемся получить семафор с таймаутом
            try:
                async with asyncio.timeout(self._semaphore_timeout):
                    async with self._semaphore:
                        logger.info(f"Acquired semaphore for bot {bot_id} (task {task_id})")
                        await self._execute_with_lock(bot_id)
            except asyncio.TimeoutError:
                logger.error(f"Timeout waiting for semaphore for bot {bot_id} (task {task_id})")
                raise
        finally:
            self._active_tasks.remove(task_id)
            logger.info(f"Finished notification for bot {bot_id} (task {task_id}, remaining tasks: {len(self._active_tasks)})")

    async def _execute_with_lock(self, bot_id: int) -> None:
        """
        Execute the usecase with acquired lock.
        """
        # Get the bot
        bot = await self._bot_repository.read_by_id(bot_id)
        if not bot:
            return

        messages = await self._message_repository.read_by_bot_and_filter_by_created(
            bot.id, bot.last_notified_at
        )

        if len(messages) == 0:
            print("NO MESSAGES")
            return

        summarized_messages = await self._workflow.start_workflow(
            bot.id, bot.description.value, messages
        )

        print("--- MESSAGE RETURN ---")
        print(summarized_messages)
        if len(summarized_messages) == 0:
            return

        # Save summaries to the database
        await self._summary_repository.create_many(bot.id, summarized_messages)

        # Get list of users for this bot
        user_ids = await self._user_bot_repository.get_users_by_bot_id(bot_id)
        if not user_ids:
            logger.warning(f"No users found for bot {bot_id}")
            return

        aiogram_bot = Bot(token=bot.token.value)

        try:
            for message in summarized_messages:
                message_text = "**" + message.title + "**" + "\n\n" + message.content

                # Extract attachments from metadata
                attachments = []
                if message.metadata and "attachments" in message.metadata:
                    attachments = message.metadata["attachments"]

                for user_id in user_ids:
                    try:
                        if attachments:
                            # Group attachments by type
                            photos = [
                                att for att in attachments if att.get("type") == "photo"
                            ]
                            # Videos are documents with video MIME type
                            videos = [
                                att
                                for att in attachments
                                if att.get("type") == "document"
                                and att.get("mime_type", "").startswith("video/")
                            ]
                            # Other documents (not videos)
                            documents = [
                                att
                                for att in attachments
                                if att.get("type") == "document"
                                and not att.get("mime_type", "").startswith("video/")
                            ]

                            downloaded_files = []

                            try:
                                # Handle media group (photos and videos together)
                                media_group: list[
                                    InputMediaPhoto | InputMediaVideo
                                ] = []
                                has_media = False

                                # Add photos to media group
                                for i, photo in enumerate(photos):
                                    photo_path = (
                                        await self._telegram_repository.download_media(
                                            channel_username=photo["channel_username"],
                                            message_id=photo["message_id"],
                                            file_name=photo["file_name"],
                                        )
                                    )
                                    downloaded_files.append(photo_path)
                                    has_media = True

                                    # First media gets the caption
                                    caption = (
                                        message_text if len(media_group) == 0 else None
                                    )
                                    media_group.append(
                                        InputMediaPhoto(
                                            media=FSInputFile(photo_path),
                                            caption=caption,
                                            parse_mode=ParseMode.MARKDOWN,
                                        )
                                    )

                                # Add videos to media group
                                for i, video in enumerate(videos):
                                    video_path = (
                                        await self._telegram_repository.download_media(
                                            channel_username=video["channel_username"],
                                            message_id=video["message_id"],
                                            file_name=video["file_name"],
                                        )
                                    )
                                    downloaded_files.append(video_path)
                                    has_media = True

                                    # First media gets the caption
                                    caption = (
                                        message_text if len(media_group) == 0 else None
                                    )
                                    media_group.append(
                                        InputMediaVideo(
                                            media=FSInputFile(video_path),
                                            caption=caption,
                                            parse_mode=ParseMode.MARKDOWN,
                                        )
                                    )

                                # Send media group if we have photos or videos
                                if has_media:
                                    if len(media_group) > 1:
                                        await aiogram_bot.send_media_group(
                                            chat_id=user_id, media=media_group
                                        )
                                    else:
                                        # Single photo
                                        if isinstance(media_group[0], InputMediaPhoto):
                                            await aiogram_bot.send_photo(
                                                chat_id=user_id,
                                                photo=media_group[0].media,
                                                caption=message_text,
                                                parse_mode=ParseMode.MARKDOWN,
                                            )
                                        # Single video
                                        else:
                                            await aiogram_bot.send_video(
                                                chat_id=user_id,
                                                video=media_group[0].media,
                                                caption=message_text,
                                                parse_mode=ParseMode.MARKDOWN,
                                            )

                                # Handle other documents (not in media group)
                                for doc in documents:
                                    file_path = (
                                        await self._telegram_repository.download_media(
                                            channel_username=doc["channel_username"],
                                            message_id=doc["message_id"],
                                            file_name=doc["file_name"],
                                        )
                                    )
                                    downloaded_files.append(file_path)

                                    await aiogram_bot.send_document(
                                        chat_id=user_id,
                                        document=FSInputFile(file_path),
                                        caption=message_text,
                                        parse_mode=ParseMode.MARKDOWN,
                                    )

                                # If we only have documents (no photos/videos), send text first
                                if not has_media and documents:
                                    await aiogram_bot.send_message(
                                        chat_id=user_id,
                                        text=message_text,
                                        parse_mode=ParseMode.MARKDOWN,
                                    )

                            finally:
                                # Clean up downloaded files
                                for file_path in downloaded_files:
                                    try:
                                        if os.path.exists(file_path):
                                            os.remove(file_path)
                                    except Exception as e:
                                        logger.error(
                                            f"Failed to delete file {file_path}: {str(e)}"
                                        )

                        else:
                            # If no attachments, just send text message
                            await aiogram_bot.send_message(
                                chat_id=user_id,
                                text=message_text,
                                parse_mode=ParseMode.MARKDOWN,
                            )

                        logger.info(
                            f"Sent notification to user {user_id} for bot {bot_id}"
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to send message to user {user_id}: {str(e)}"
                        )

            # Update last_notified_at timestamp
            await self._bot_repository.update_last_notified_at(bot.id, datetime.now())

        except Exception as e:
            logger.error(f"Error in notify_bot_usecase: {str(e)}")
            raise e

        finally:
            # Close bot session
            await aiogram_bot.session.close()
