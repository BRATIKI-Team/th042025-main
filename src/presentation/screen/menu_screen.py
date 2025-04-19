from aiogram import Router, F
from aiogram.types import CallbackQuery
from dishka import FromDishka

from src.application.usecase.bot.has_bot_usecase import HasBotUsecase
from src.presentation.kb.start_kb import start_kb


router = Router()


@router.callback_query(F.data.startswith("menu"))
async def menu_screen(
    callback: CallbackQuery, has_bot_usecase: FromDishka[HasBotUsecase]
) -> None:
    user_id = callback.from_user.id
    has_bot = await has_bot_usecase.execute(user_id=user_id)
    new_message = callback.data.split("_")[-1] == "new"

    text = "Добро пожаловать в бота!\n\n" "Выберите интересующий вас пункт меню."

    if new_message:
        await callback.message.answer(text=text, reply_markup=start_kb(has_bot=has_bot))
    else:
        await callback.message.edit_text(
            text=text, reply_markup=start_kb(has_bot=has_bot)
        )
