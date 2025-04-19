from aiogram import Router, F
from aiogram.types import CallbackQuery
from dishka import FromDishka

from src.application.usecase.bot.get_my_bots_usecase import GetMyBotsUsecase
from src.domain.enum.bot_status_enum import BotStatus
from src.presentation.kb.manage_bot_kb import manage_bot_kb
from src.presentation.kb.to_menu_kb import to_menu_kb


router = Router()


@router.callback_query(F.data.startswith("manage_bot"))
async def manage_bot(
    callback: CallbackQuery, get_my_bots_usecase: FromDishka[GetMyBotsUsecase]
):
    try:
        page = int(callback.data.split("_")[-1])
    except Exception:
        page = 1

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
