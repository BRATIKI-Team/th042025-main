from datetime import datetime
from src.application.dto.bot_detail_response import BotDetailResponse
from src.application.dto.bot_light_response import BotLightResponse
from src.application.mapper.source_mapper import SourceMapper
from src.domain.model.bot_model import BotModel
from src.domain.model.source_model import SourceModel


class BotMapper:
    @staticmethod
    def to_light_response(bot: BotModel) -> BotLightResponse:
        return BotLightResponse(
            id=bot.id,
            name=bot.title.value,
            topic=bot.description.value,
            status=bot.status,
        )

    @staticmethod
    def to_detail_response(
        bot: BotModel,
        sources: list[SourceModel],
        users_count: int,
        metrics: dict[str, int],
    ) -> BotDetailResponse:
        return BotDetailResponse(
            id=bot.id,
            name=bot.title.value,
            topic=bot.description.value,
            status=bot.status,
            users_count=users_count,
            sources=[SourceMapper.to_response(source) for source in sources],
            metrics=metrics,
        )
