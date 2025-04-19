from datetime import datetime
from typing import List

from src.application.agents.source_searcher import SourceSearcherAgent
from src.application.agents.topic_validator.topic_validator_agent import (
    TopicValidatorAgent,
)
from src.domain.enum.source_status_enum import SourceStatus
from src.domain.enum.source_type_enum import SourceType
from src.domain.model.grouped_source_model import GroupedSourceModel
from src.domain.model.source_model import SourceModel
from src.domain.repository.source_repository import SourceRepository
from src.infrastructure.dao.source_dao import SourceDAO


class SourceRepositoryImpl(SourceRepository):
    def __init__(
        self,
        validate_topic_agent: TopicValidatorAgent,
        search_sources_agent: SourceSearcherAgent,
    ):
        self.__validate_topic_agent = validate_topic_agent
        self.__search_sources_agent = search_sources_agent

    async def get_source_by_status(self, status: SourceStatus) -> SourceModel | None:
        dao = await SourceDAO.objects().get(SourceDAO.status == status.value).first()

        if dao is None:
            return None

        return SourceDAO.from_dao(dao)

    async def get_grouped_sources_by_notification_period(
        self,
    ) -> List[GroupedSourceModel]:
        # Get all sources with their associated bots using joins
        sources = await SourceDAO.select(
            SourceDAO.id,
            SourceDAO.url,
            SourceDAO.type,
            SourceDAO.last_hit_datetime,
            SourceDAO.bot_id._.id,
            SourceDAO.bot_id._.notification_period,
            SourceDAO.bot_id._.last_notified_at,
        )

        # Group sources by type and url
        grouped_sources = {}

        for source in sources:
            # Access dictionary keys instead of attributes
            source_type = source["type"]
            source_url = source["url"]
            source_id = source["id"]
            bot_id = source["bot_id.id"]
            notification_period = source["bot_id.notification_period"]
            last_notified_at = source["bot_id.last_notified_at"]
            last_hit_datetime = source["last_hit_datetime"]

            key = (source_type, source_url)

            if key not in grouped_sources:
                grouped_sources[key] = {
                    "url": source_url,
                    "type": source_type,
                    "sources": [],
                    "notification_periods": [],
                    "last_hit_datetimes": [],
                }

            # Add source data to the group
            grouped_sources[key]["sources"].append(
                {
                    "id": source_id,
                    "bot_id": bot_id,
                    "bot_notification_period": notification_period,
                    "bot_last_notified_at": last_notified_at,
                }
            )
            grouped_sources[key]["notification_periods"].append(notification_period)

            if last_hit_datetime:
                grouped_sources[key]["last_hit_datetimes"].append(last_hit_datetime)

        # Convert to GroupedSourceModel
        result = []

        for key, data in grouped_sources.items():
            # Get the minimum notification period
            min_notification_period = min(data["notification_periods"])

            # Get the earliest last_hit_datetime or current time if none exists
            last_hit_datetime = None
            if data["last_hit_datetimes"]:
                last_hit_datetime = min(data["last_hit_datetimes"])
            else:
                last_hit_datetime = datetime.now()

            result.append(
                GroupedSourceModel(
                    url=data["url"],
                    type=data["type"],
                    sources=data["sources"],
                    last_hit_datetime=last_hit_datetime,
                    notification_period=min_notification_period,
                )
            )

        return result

    async def update_last_hit_datetime(self, source_ids: List[int]) -> None:
        current_time = datetime.now()

        for source_id in source_ids:
            await SourceDAO.update({SourceDAO.last_hit_datetime: current_time}).where(
                SourceDAO.id == source_id
            )

    async def validate_topic(self, topic: str) -> bool:
        return await self.__validate_topic_agent.execute(topic=topic)

    async def search_sources(self, bot_id: int, topic: str) -> None:
        responses = await self.__search_sources_agent.execute(topic=topic)

        models = []
        for response in responses:
            models.append(
                SourceDAO(
                    bot_id=bot_id,
                    url=response.url,
                    type=SourceType.TG.value,
                    status=SourceStatus.PENDING.value,
                    description=response.description,
                    name=response.url,
                )
            )

        await SourceDAO.insert(*models)

    async def change_status(self, id: int, status: SourceStatus) -> None:
        await SourceDAO.update({SourceDAO.status: status.value}).where(
            SourceDAO.id == id
        )
