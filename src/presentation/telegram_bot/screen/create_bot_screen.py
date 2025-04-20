from typing import cast
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka

from src.application.dto.create_bot_request import CreateBotRequest
from src.application.usecase.bot.create_bot_usecase import CreateBotUsecase
from src.application.usecase.bot.is_token_unqiue_usecase import IsTokenUniqueUsecase
from src.application.usecase.source.accept_source_usecase import AcceptSourceUsecase
from src.application.usecase.source.get_pending_source_usecase import (
    GetPendingSourceUsecase,
)
from src.application.usecase.source.reject_source_usecase import RejectSourceUsecase
from src.application.usecase.source.search_sources_usecase import SearchSourcesUsecase
from src.application.usecase.source.validate_topic_usecase import ValidateTopicUsecase
from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod
from src.domain.value_object.bot_description_vo import BotDescriptionVO
from src.domain.value_object.bot_name_vo import BotNameVO
from src.domain.value_object.bot_token_vo import BotTokenVO
from src.presentation.telegram_bot.kb.bot_notification_period_kb import (
    bot_notification_period_kb,
)
from src.presentation.telegram_bot.kb.select_sources_kb import select_sources_kb
from src.presentation.telegram_bot.kb.source_kb import source_kb
from src.presentation.telegram_bot.kb.to_menu_kb import to_menu_kb

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
    text = (
        "🔩 Шаг 1/5\n\n"
        "Введите название бота в нашей системе.\n\n"
        "Если вы хотите остановить создание бота, введите команду /cancel"
    )

    await bot.edit_message_text(
        text=text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    await state.set_state(CreateBotStatesGroup.bot_name)


@router.message(CreateBotStatesGroup.bot_name)
async def bot_name_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.text.strip() == "/cancel":
        return await cancel_handler(message, state)

    try:
        bot_name = BotNameVO(value=message.text.strip())
    except ValueError:
        await bot.send_message(
            text=f"Ошибка. Возможно, вы ввели слишком длинное название бота. Попробуйте снова.",
            chat_id=message.chat.id,
        )
        return

    text = (
        "⚙️ Шаг 2/5\n\n"
        "Введите описание бота, по которому будут выбираться источники данных. Будьте точны и лаконичны.\n\n"
        "Если вы хотите остановить создание бота, введите команду /cancel"
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
    if message.text.strip() == "/cancel":
        return await cancel_handler(message, state)

    try:
        bot_description = BotDescriptionVO(value=message.text.strip())
    except ValueError:
        text = (
            "Ошибка. Возможно, вы ввели слишком длинное описание бота. Попробуйте снова.\n\n"
            "Если вы хотите остановить создание бота, введите команду /cancel"
        )

        await bot.send_message(
            text=text,
            chat_id=message.chat.id,
        )
        return

    if not await validate_topic_usecase.execute(topic=bot_description.value):
        text = (
            "Ошибка. Пожалуйста, введите более подробное описание бота.\n\n"
            "Если вы хотите остановить создание бота, введите команду /cancel"
        )

        await bot.send_message(
            text=text,
            chat_id=message.chat.id,
        )
        return

    text = (
        "🔋 Шаг 3/5\n\n"
        "Выберите период, за который будет формироваться сводка новостей.\n\n"
        "Если вы хотите остановить создание бота, введите команду /cancel"
    )

    await bot.send_message(
        text=text,
        chat_id=message.chat.id,
        reply_markup=bot_notification_period_kb(),
    )

    await state.update_data(bot_description=bot_description)
    await state.set_state(CreateBotStatesGroup.bot_notification_period)


@router.message(CreateBotStatesGroup.bot_notification_period)
async def bot_notification_period_message_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if message.text.strip() == "/cancel":
        return await cancel_handler(message, state)


@router.callback_query(CreateBotStatesGroup.bot_notification_period)
async def bot_notification_period_callback_query_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
) -> None:
    period = BotNotificationPeriod(int(callback_query.data))

    # TODO better instructions

    text = (
        "🧠 Шаг 4/5\n\n"
        "Введите токен для бота. Создать своего бота можно здесь -> @BotFather.\n\n"
        "Для этого напишите боту /start, а потом /newbot\n"
        "Следуйте инструкциям в боте (Введите имя бота и его юзернейм)\n"
        "После этого вам отправят токен - он выглядит примерно так 7948438110:AAE5LFveabRGTufd20YnrvA2K-qwKQgpmJQ\n"
        "Скопируйте его и отправьте нам\n\n"
        "Если вы хотите остановить создание бота, введите команду /cancel"
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
    is_token_unique_usecase: FromDishka[IsTokenUniqueUsecase],
) -> None:
    if message.text.strip() == "/cancel":
        return await cancel_handler(message, state)

    try:
        bot_token = BotTokenVO(value=message.text.strip())
    except ValueError:
        text = (
            "Ошибка. Возможно, вы ввели неверный токен. Пожалуйста, обратитесь к инструкции и попробуйте снова.\n\n"
            "Если вы хотите остановить создание бота, введите команду /cancel"
        )

        await bot.send_message(
            text=text,
            chat_id=message.chat.id,
        )
        return

    if not await is_token_unique_usecase.execute(token=bot_token.value):
        text = (
            "Ошибка. Токен уже используется другим ботом. Пожалуйста, попробуйте другой токен.\n\n"
            "Если вы хотите остановить создание бота, введите команду /cancel"
        )

        await bot.send_message(
            text=text,
            chat_id=message.chat.id,
        )
        return

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
        "🤖 Шаг 5/5\n\n"
        "Выберите источники данных, по которым будет формироваться сводка новостей. Вам нужно выбрать хотя бы один источник."
    )

    await bot.send_message(
        text=text,
        chat_id=message.chat.id,
        reply_markup=select_sources_kb(),
    )

    await state.update_data(
        bot_id=bot_id, bot_token=bot_token, approved_at_least_one_source=False
    )
    await state.set_state(CreateBotStatesGroup.bot_sources)


@router.callback_query(F.data == "select_sources")
async def select_sources_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    get_pending_source_usecase: FromDishka[GetPendingSourceUsecase],
    search_sources_usecase: FromDishka[SearchSourcesUsecase],
) -> None:
    bot_id = cast(int, await state.get_value("bot_id"))
    approved_at_least_one_source = cast(
        bool, await state.get_value("approved_at_least_one_source")
    )

    pending_source = await get_pending_source_usecase.execute(bot_id=bot_id)

    if pending_source is None:
        await search_sources_usecase.execute(bot_id=bot_id)

        pending_source = await get_pending_source_usecase.execute(bot_id=bot_id)

    if pending_source is None:
        text = "🤖 Шаг 5/5\n\n" "Нет доступных источников данных. Попробуйте позже."

        await callback_query.message.edit_text(
            text=text,
            reply_markup=select_sources_kb(
                text="Обновить список источников",
                can_stop_searching=approved_at_least_one_source,
            ),
        )

        return

    text = (
        f"🤖 Шаг 5/5\n\n"
        f"Источник данных: {pending_source.name}\n\n"
        f"Описание: {pending_source.description}\n\n"
        f"Ссылка: {pending_source.url}\n\n"
    )

    await callback_query.message.edit_text(
        text=text,
        reply_markup=source_kb(
            source_id=pending_source.id, can_stop_searching=approved_at_least_one_source
        ),
    )


@router.callback_query(F.data.startswith("accept_source_"))
async def accept_source_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    accept_source_usecase: FromDishka[AcceptSourceUsecase],
) -> None:
    source_id = int(callback_query.data.split("_")[-1])

    await accept_source_usecase.execute(source_id=source_id)

    await state.update_data(approved_at_least_one_source=True)

    text = (
        "🤖 Шаг 5/5\n\n"
        "Источник данных принят. Вы можете принять ещё один источник или остановить поиск."
    )

    await callback_query.message.edit_text(
        text=text,
        reply_markup=select_sources_kb(
            text="🕵️‍♂️ Продолжить выбор источников", can_stop_searching=True
        ),
    )


@router.callback_query(F.data.startswith("reject_source_"))
async def reject_source_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    reject_source_usecase: FromDishka[RejectSourceUsecase],
) -> None:
    source_id = int(callback_query.data.split("_")[-1])

    await reject_source_usecase.execute(source_id=source_id)

    approved_at_least_one_source = cast(
        bool, await state.get_value("approved_at_least_one_source")
    )

    text = (
        "🤖 Шаг 5/5\n\n" "Источник данных отклонен."
        if not approved_at_least_one_source
        else "Источник данных отклонен. Вы можете продолжить выбор источников или остановить поиск."
    )

    await callback_query.message.edit_text(
        text=text,
        reply_markup=select_sources_kb(
            text="🕵️‍♂️ Продолжить выбор источников",
            can_stop_searching=approved_at_least_one_source,
        ),
    )


async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(
        text="😢 Создание бота отменено.",
        reply_markup=to_menu_kb(),
    )
