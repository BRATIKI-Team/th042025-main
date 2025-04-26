from typing import List
from fastapi import FastAPI, Request
from dishka.integrations.fastapi import (
    FastapiProvider,
    FromDishka,
    setup_dishka,
    inject,
)
from fastapi.middleware.cors import CORSMiddleware
from aiogram.types import Update

from src.application.dto.bot_detail_response import BotDetailResponse
from src.application.dto.bot_light_response import BotLightResponse
from src.application.usecase.bot.get_all_bots_usecase import GetAllBotsUsecase
from src.application.usecase.bot.get_detail_bot_usecase import GetDetailBotUsecase
from src.application.usecase.tg.webhook_usecase import WebhookUsecase
from src.di.container import init_container

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/bots/{bot_id}/actions/webhook")
@inject
async def webhook(
    bot_id: int,
    request: Request,
    webhook_usecase: FromDishka[WebhookUsecase],
) -> None:
    return await webhook_usecase.execute(
        bot_id=bot_id, update=Update(**await request.json())
    )
