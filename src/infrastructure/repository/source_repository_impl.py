from datetime import datetime
from typing import List

from src.application.agents.source_searcher import SourceSearcherAgent
from src.application.agents.topic_validator.topic_validator_agent import (
    TopicValidatorAgent,
)
from src.application.dto.source_generate_response import SourceGenerateResponse
from src.domain.enum.source_status_enum import SourceStatus
from src.domain.enum.source_type_enum import SourceType
from src.domain.model.pagination_model import PaginationModel
from src.domain.model.source_model import SourceModel
from src.domain.repository.source_repository import SourceRepository
from src.domain.repository.telegram_repository import TelegramRepository
from src.infrastructure.dao.source_dao import SourceDAO
from src.infrastructure.utils.backoff import backoff


class SourceRepositoryImpl(SourceRepository):
    def __init__(
        self,
        validate_topic_agent: TopicValidatorAgent,
        search_sources_agent: SourceSearcherAgent,
        telegram_repository: TelegramRepository,
    ):
        self.__validate_topic_agent = validate_topic_agent
        self.__search_sources_agent = search_sources_agent
        self.__telegram_repository = telegram_repository

    async def get_source_by_status(
        self, bot_id: int, status: SourceStatus
    ) -> SourceModel | None:
        dao = (
            await SourceDAO.objects()
            .get((SourceDAO.status == status.value) & (SourceDAO.bot_id == bot_id))
            .first()
        )

        if dao is None:
            return None

        return SourceDAO.from_dao(dao)

    async def update_last_hit_datetime(self, source_ids: List[int]) -> None:
        current_time = datetime.now()

        for source_id in source_ids:
            await SourceDAO.update({SourceDAO.last_hit_datetime: current_time}).where(
                SourceDAO.id == source_id
            )

    async def validate_topic(self, topic: str) -> bool:
        return await self.__validate_topic_agent.execute(topic=topic)

    async def search_sources(self, bot_id: int, topic: str) -> None:
        sources = await self.__search_sources_agent.execute(topic=topic)
        filtered_sources = await self._get_filtered_source(sources)

        models = []
        for source in filtered_sources:
            models.append(
                SourceDAO(
                    bot_id=bot_id,
                    url=source.url,
                    type=SourceType.TG.value,
                    status=SourceStatus.PENDING.value,
                    description=source.description,
                    name=source.url,
                )
            )

        await SourceDAO.insert(*models)

    @backoff(
        exception=Exception,
        max_tries=5,
        max_time=60,
        initial_delay=1.0,
        exponential_base=2.0,
    )
    async def _get_filtered_source(
        self, sources: List[SourceGenerateResponse]
    ) -> List[SourceGenerateResponse]:
        result = []
        for source in sources:
            try:
                await self.__telegram_repository.get_channel_info(source.url)
                result.append(source)
            except Exception:
                continue

        return result

    async def change_status(self, id: int, status: SourceStatus) -> None:
        await SourceDAO.update({SourceDAO.status: status.value}).where(
            SourceDAO.id == id
        )

    async def has_rejected_source(self, bot_id: int) -> bool:
        return await SourceDAO.exists().where(
            (SourceDAO.status == SourceStatus.REJECTED.value)
            & (SourceDAO.bot_id == bot_id)
        )

    async def has_accepted_source(self, bot_id: int) -> bool:
        return await SourceDAO.exists().where(
            (SourceDAO.status == SourceStatus.ACCEPTED.value)
            & (SourceDAO.bot_id == bot_id)
        )

    async def get_bot_sources(
        self, bot_id: int, status: SourceStatus, page: int, page_size: int
    ) -> PaginationModel[SourceModel]:
        query = (
            await SourceDAO.objects()
            .where((SourceDAO.bot_id == bot_id) & (SourceDAO.status == status.value))
            .offset((page - 1) * page_size)
            .limit(page_size + 1)
        )

        models = [SourceDAO.from_dao(dao) for dao in query]
        has_more = len(models) > page_size

        return PaginationModel(
            items=models[:page_size],
            has_more=has_more,
            page=page,
            page_size=page_size,
        )

    async def get_by_bot_id(self, bot_id: int) -> List[SourceModel]:
        daos = await SourceDAO.objects().where(SourceDAO.bot_id == bot_id)

        return [SourceDAO.from_dao(dao) for dao in daos]
