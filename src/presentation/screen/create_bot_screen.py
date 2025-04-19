from typing import cast
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka

from src.application.dto.create_bot_request import CreateBotRequest
from src.application.usecase.bot.create_bot_usecase import CreateBotUsecase
from src.application.usecase.source.get_pending_source_usecase import GetPendingSourceUsecase
from src.application.usecase.source.validate_topic_usecase import ValidateTopicUsecase
from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.value_object.bot_name_vo import BotNameVO
from src.domain.value_object.bot_token_vo import BotTokenVO
from src.presentation.kb.bot_notification_period_kb import bot_notification_period_kb
from src.presentation.kb.select_sources_kb import select_sources_kb

router = Router()


class CreateBotStatesGroup(StatesGroup):
    bot_name = State()
    bot_description = State()
    bot_notification_period = State()
    bot_token = State()
    bot_sources = State()


@router.callback_query(F.data == "create_bot")
async def create_bot_screen(
    callback_query: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    text = "Шаг 1/5\n\n" "Введите название бота в нашей системе."

    await bot.edit_message_text(
        text=text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    await state.set_state(CreateBotStatesGroup.bot_name)


@router.message(CreateBotStatesGroup.bot_name)
async def bot_name_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    try:
        bot_name = BotNameVO(value=message.text.strip())
    except ValueError as e:
        await bot.send_message(
            text=f"Ошибка. Возможно, вы ввели слишком длинное название бота. Попробуйте снова.",
            chat_id=message.chat.id,
        )
        return

    text = (
        "Шаг 2/5\n\n"
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
    message: Message,
    state: FSMContext,
    bot: Bot,
    validate_topic_usecase: FromDishka[ValidateTopicUsecase],
) -> None:
    try:
        bot_description = BotDescriptionVO(value=message.text.strip())
    except ValueError as e:
        await bot.send_message(
            text=f"Ошибка. Возможно, вы ввели слишком длинное описание бота. Попробуйте снова.",
            chat_id=message.chat.id,
        )
        return

    if not await validate_topic_usecase.execute(topic=bot_description.value):
        await bot.send_message(
            text=f"Ошибка. Пожалуйста, введите более подробное описание бота.",
            chat_id=message.chat.id,
        )
        return

    text = (
        "Шаг 3/5\n\n" "Выберите период, за который будет формироваться сводка новостей."
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
    callback_query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
) -> None:
    period = BotNotificationPeriod(int(callback_query.data))

    # TODO better instructions

    text = (
        "Шаг 4/5\n\n" "Введите токен для бота. Токен можно получить в боте @BotFather."
    )

    await bot.send_message(
        text=text,
        chat_id=callback_query.message.chat.id,
    )

    await state.update_data(bot_notification_period=period)
    await state.set_state(CreateBotStatesGroup.bot_token)


@router.message(CreateBotStatesGroup.bot_token)
async def bot_token_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    create_bot_usecase: FromDishka[CreateBotUsecase],
) -> None:
    try:
        bot_token = BotTokenVO(value=message.text.strip())
    except ValueError as e:
        await bot.send_message(
            text=f"Ошибка. Возможно, вы ввели неверный токен. Пожалуйста, обратитесь к инструкции и попробуйте снова.",
            chat_id=message.chat.id,
        )
        return

    # TODO check if bot token is valid

    bot_id = await create_bot_usecase.execute(
        request=CreateBotRequest(
            user_id=message.from_user.id,
            name=cast(BotNameVO, await state.get_value("bot_name")),
            period=cast(
                BotNotificationPeriod, await state.get_value("bot_notification_period")
            ),
            token=bot_token,
            description=cast(
                BotDescriptionVO, await state.get_value("bot_description")
            ),
        )
    )

    text = (
        "Шаг 5/5\n\n"
        "Выберите источники данных, по которым будет формироваться сводка новостей. Вам нужно выбрать хотя бы один источник."
    )

    await bot.send_message(
        text=text,
        chat_id=message.chat.id,
        reply_markup=select_sources_kb(),
    )

    await state.update_data(bot_id=bot_id, bot_token=bot_token)
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
