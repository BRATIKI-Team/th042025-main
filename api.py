from typing import List
from fastapi import APIRouter, FastAPI
from dishka.integrations.fastapi import (
    FastapiProvider,
    FromDishka,
    setup_dishka,
    inject,
)

from src.application.dto.bot_detail_response import BotDetailResponse
from src.application.dto.bot_light_response import BotLightResponse
from src.application.usecase.bot.get_all_bots_usecase import GetAllBotsUsecase
from src.application.usecase.bot.get_detail_bot_usecase import GetDetailBotUsecase
from src.di.container import init_container

app = FastAPI()
container = init_container(specific_providers=[FastapiProvider()])
setup_dishka(container, app)


@app.get("/bots/")
@inject
async def get_bots(
    get_all_bots_usecase: FromDishka[GetAllBotsUsecase],
) -> List[BotLightResponse]:
    return await get_all_bots_usecase.execute()


@app.get("/bots/{bot_id}/")
@inject
async def get_bot(
    bot_id: int, get_detail_bot_usecase: FromDishka[GetDetailBotUsecase]
) -> BotDetailResponse:
    return await get_detail_bot_usecase.execute(bot_id=bot_id)
