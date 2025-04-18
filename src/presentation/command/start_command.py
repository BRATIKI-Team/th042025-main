from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dishka import FromDishka

from src.application.usecase.has_bot_usecase import HasBotUsecase
from src.presentation.kb.start_kb import start_kb

router = Router()


@router.message(Command("start"))
async def start_command(
    message: Message, has_bot_usecase: FromDishka[HasBotUsecase]
) -> None:
    user_id = message.from_user.id
    has_bot = await has_bot_usecase.execute(user_id=user_id)

    text = (
        (
            "Привет! Я ботик, который может создавать контент для телеграмм-ботов на основе определенных тем.\n\n",
            "Меня создали славные ребята - BRATIKI\n\n",
            "Я умею создавать контент для телеграмм-ботов на основе определенных тем.\n\n",
            "Чтобы я мог тебе помочь, нажми на кнопку ниже!",
        )
        if not has_bot
        else (
            "Добро пожаловать в бота!\n\n",
            "Выберите интересующий вас пункт меню.",
        )
    )

    await message.answer(text=text, reply_markup=start_kb(has_bot=has_bot))
