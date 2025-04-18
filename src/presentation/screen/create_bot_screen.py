from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka

from src.application.usecase.get_pending_source_usecase import GetPendingSourceUsecase
from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.value_object.bot_name_vo import BotNameVO
from src.presentation.kb.bot_notification_period_kb import bot_notification_period_kb
from src.presentation.kb.select_sources_kb import select_sources_kb

router = Router()


class CreateBotStatesGroup(StatesGroup):
    bot_name = State()
    bot_description = State()
    bot_notification_period = State()
    bot_sources = State()


@router.callback_query(F.data == "create_bot")
async def create_bot_screen(
    callback_query: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    text = "Шаг 1/4\n\n" "Введите название бота в нашей системе."

    await bot.edit_message_text(
        text=text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    await state.set_state(CreateBotStatesGroup.bot_name)


@router.message(CreateBotStatesGroup.bot_name)
async def bot_name_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    try:
        bot_name = BotNameVO(name=message.text.strip())
    except ValueError as e:
        await bot.send_message(
            text=f"Ошибка. Возможно, вы ввели слишком длинное название бота. Попробуйте снова.",
            chat_id=message.chat.id,
        )
        return

    text = (
        "Шаг 2/4\n\n"
        "Введите описание бота, по которому будут выбираться источники данных. Будьте точны и лаконичны."
    )

    await bot.send_message(
        text=text,
        chat_id=message.chat.id,
    )

    await state.update_data(bot_name=bot_name)
    await state.set_state(CreateBotStatesGroup.bot_description)


@router.message(CreateBotStatesGroup.bot_description)
async def bot_description_handler(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    try:
        bot_description = BotDescriptionVO(description=message.text.strip())
    except ValueError as e:
        await bot.send_message(
            text=f"Ошибка. Возможно, вы ввели слишком длинное описание бота. Попробуйте снова.",
            chat_id=message.chat.id,
        )
        return

    text = (
        "Шаг 3/4\n\n" "Выберите период, за который будет формироваться сводка новостей."
    )

    await bot.send_message(
        text=text,
        chat_id=message.chat.id,
        reply_markup=bot_notification_period_kb(),
    )

    await state.update_data(bot_description=bot_description)
    await state.set_state(CreateBotStatesGroup.bot_notification_period)


@router.callback_query(CreateBotStatesGroup.bot_notification_period)
async def bot_notification_period_handler(
    callback_query: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    period = BotNotificationPeriod(int(callback_query.data))

    text = (
        "Шаг 4/4\n\n"
        "Выберите источники данных, по которым будет формироваться сводка новостей. Вам нужно выбрать хотя бы один источник."
    )

    await bot.send_message(
        text=text,
        chat_id=callback_query.message.chat.id,
        reply_markup=select_sources_kb(),
    )

    await state.update_data(bot_notification_period=period)
    await state.set_state(CreateBotStatesGroup.bot_sources)


@router.callback_query(F.data == "select_sources")
async def select_sources_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    get_pending_source_usecase: FromDishka[GetPendingSourceUsecase],
) -> None:
    pending_source = await get_pending_source_usecase.execute()

    if pending_source is None:
        await bot.send_message(
            text="Нет доступных источников данных. Попробуйте позже.",
            chat_id=callback_query.message.chat.id,
        )
        return
