from aiogram import Router, F
from aiogram.types import CallbackQuery
from dishka import FromDishka

from src.application.usecase.bot.delete_bot_usecase import DeleteBotUsecase
from src.application.usecase.bot.get_my_bots_usecase import GetMyBotsUsecase
from src.application.usecase.bot.resume_bot_usecase import ResumeBotUsecase
from src.application.usecase.bot.stop_bot_usecase import StopBotUsecase
from src.domain.enum.bot_status_enum import BotStatus
from src.presentation.telegram_bot.kb.manage_bot_kb import manage_bot_kb
from src.presentation.telegram_bot.kb.to_menu_kb import to_menu_kb


router = Router()


async def manage_bot_panel(
    page: int, callback: CallbackQuery, get_my_bots_usecase: GetMyBotsUsecase
):
    pagination = await get_my_bots_usecase.execute(
        user_id=callback.from_user.id, page=page
    )

    model = pagination.items[0] if len(pagination.items) != 0 else None

    if model is None:
        await callback.message.edit_text(
            text="У вас нет ботов. Создайте бота, чтобы начать работу.",
            reply_markup=to_menu_kb(),
        )
        return

    text = (
        f"Бот: {model.title.value}\n\n"
        f"Описание: {model.description.value}\n\n"
        f"Статус: {'Активный' if model.status.value == BotStatus.ACTIVE.value else 'Неактивный'}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=manage_bot_kb(
            bot_id=model.id,
            page=page,
            is_bot_paused=model.status.value == BotStatus.INACTIVE.value,
            has_next=pagination.has_more,
            has_previous=page != 1,
        ),
    )


@router.callback_query(F.data.startswith("manage_bot"))
async def manage_bot(
    callback: CallbackQuery, get_my_bots_usecase: FromDishka[GetMyBotsUsecase]
):
    try:
        page = int(callback.data.split("_")[-1])
    except Exception:
        page = 1

    await manage_bot_panel(
        page=page, callback=callback, get_my_bots_usecase=get_my_bots_usecase
    )


@router.callback_query(F.data.startswith("resume_bot"))
async def resume_bot(
    callback: CallbackQuery,
    resume_bot_usecase: FromDishka[ResumeBotUsecase],
    get_my_bots_usecase: FromDishka[GetMyBotsUsecase],
):
    bot_id = int(callback.data.split("_")[-1])
    page = int(callback.data.split("_")[-2])

    await resume_bot_usecase.execute(bot_id=bot_id)

    await manage_bot_panel(
        page=page, callback=callback, get_my_bots_usecase=get_my_bots_usecase
    )


@router.callback_query(F.data.startswith("pause_bot"))
async def pause_bot(
    callback: CallbackQuery,
    stop_bot_usecase: FromDishka[StopBotUsecase],
    get_my_bots_usecase: FromDishka[GetMyBotsUsecase],
):
    bot_id = int(callback.data.split("_")[-1])
    page = int(callback.data.split("_")[-2])

    await stop_bot_usecase.execute(bot_id=bot_id)

    await manage_bot_panel(
        page=page, callback=callback, get_my_bots_usecase=get_my_bots_usecase
    )


@router.callback_query(F.data.startswith("delete_bot"))
async def delete_bot(
    callback: CallbackQuery,
    delete_bot_usecase: FromDishka[DeleteBotUsecase],
    get_my_bots_usecase: FromDishka[GetMyBotsUsecase],
):
    bot_id = int(callback.data.split("_")[-1])
    page = int(callback.data.split("_")[-2])

    await delete_bot_usecase.execute(bot_id=bot_id)

    await manage_bot_panel(
        page=min(1, page - 1),
        callback=callback,
        get_my_bots_usecase=get_my_bots_usecase,
    )
