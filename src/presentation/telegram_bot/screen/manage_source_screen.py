from aiogram import Router, F
from aiogram.types import CallbackQuery
from dishka import FromDishka

from src.application.usecase.bot.get_bot_by_id_usecase import GetBotByIdUsecase
from src.application.usecase.source.accept_source_usecase import AcceptSourceUsecase
from src.application.usecase.source.get_bot_sources_usecase import GetBotSourcesUsecase
from src.application.usecase.source.has_accepted_source_usecase import (
    HasAcceptedSourceUsecase,
)
from src.application.usecase.source.has_rejected_source_usecase import (
    HasRejectedSourceUsecase,
)
from src.application.usecase.source.reject_source_usecase import RejectSourceUsecase
from src.domain.enum.source_status_enum import SourceStatus
from src.presentation.telegram_bot.kb.change_status_source_kb import (
    change_status_source_kb,
)
from src.presentation.telegram_bot.kb.manage_source_kb import manage_source_kb
from src.presentation.telegram_bot.kb.retry_source_kb import retry_source_kb
from src.presentation.telegram_bot.kb.to_menu_kb import to_menu_kb

router = Router()


@router.callback_query(F.data.startswith("manage_sources_accepted_reject"))
async def manage_sources_accepted_reject(
    callback: CallbackQuery,
    get_bot_sources_usecase: FromDishka[GetBotSourcesUsecase],
    reject_source_usecase: FromDishka[RejectSourceUsecase],
) -> None:
    page = int(callback.data.split("_")[-1])
    bot_id = int(callback.data.split("_")[-2])

    model = (
        await get_bot_sources_usecase.execute(
            bot_id=bot_id, status=SourceStatus.ACCEPTED, page=page
        )
    ).items[0]
    await reject_source_usecase.execute(source_id=model.id)

    await manage_sources_panel(
        callback=callback,
        bot_id=bot_id,
        page=max(page - 1, 1),
        get_bot_sources_usecase=get_bot_sources_usecase,
        status=SourceStatus.ACCEPTED,
        prefix="manage_sources_accepted",
        can_accept=False,
        can_decline=True,
        can_go_next=True,
    )


@router.callback_query(F.data.startswith("manage_sources_accepted"))
async def manage_sources_accepted(
    callback: CallbackQuery, get_bot_sources_usecase: FromDishka[GetBotSourcesUsecase]
) -> None:
    page = int(callback.data.split("_")[-1])
    bot_id = int(callback.data.split("_")[-2])

    await manage_sources_panel(
        callback=callback,
        bot_id=bot_id,
        page=page,
        get_bot_sources_usecase=get_bot_sources_usecase,
        status=SourceStatus.ACCEPTED,
        prefix="manage_sources_accepted",
        can_accept=False,
        can_decline=True,
        can_go_next=True,
    )


@router.callback_query(F.data.startswith("manage_sources_declined_accept"))
async def manage_sources_declined_accept(
    callback: CallbackQuery,
    get_bot_sources_usecase: FromDishka[GetBotSourcesUsecase],
    accept_source_usecase: FromDishka[AcceptSourceUsecase],
) -> None:
    page = int(callback.data.split("_")[-1])
    bot_id = int(callback.data.split("_")[-2])

    model = (
        await get_bot_sources_usecase.execute(
            bot_id=bot_id, status=SourceStatus.REJECTED, page=page
        )
    ).items[0]
    await accept_source_usecase.execute(source_id=model.id)

    await manage_sources_panel(
        callback=callback,
        bot_id=bot_id,
        page=max(page - 1, 1),
        get_bot_sources_usecase=get_bot_sources_usecase,
        status=SourceStatus.REJECTED,
        prefix="manage_sources_declined",
        can_accept=True,
        can_decline=False,
        can_go_next=True,
    )


@router.callback_query(F.data.startswith("manage_sources_declined"))
async def manage_sources_declined(
    callback: CallbackQuery, get_bot_sources_usecase: FromDishka[GetBotSourcesUsecase]
) -> None:
    page = int(callback.data.split("_")[-1])
    bot_id = int(callback.data.split("_")[-2])

    await manage_sources_panel(
        callback=callback,
        bot_id=bot_id,
        page=page,
        get_bot_sources_usecase=get_bot_sources_usecase,
        status=SourceStatus.REJECTED,
        prefix="manage_sources_declined",
        can_accept=True,
        can_decline=False,
        can_go_next=True,
    )


@router.callback_query(F.data.startswith("manage_sources_new_accept"))
async def manage_sources_new_accept(
    callback: CallbackQuery,
    get_bot_sources_usecase: FromDishka[GetBotSourcesUsecase],
    accept_source_usecase: FromDishka[AcceptSourceUsecase],
) -> None:
    page = int(callback.data.split("_")[-1])
    bot_id = int(callback.data.split("_")[-2])

    model = (
        await get_bot_sources_usecase.execute(
            bot_id=bot_id, status=SourceStatus.PENDING, page=page
        )
    ).items[0]
    await accept_source_usecase.execute(source_id=model.id)

    await manage_sources_panel(
        callback=callback,
        bot_id=bot_id,
        page=max(page - 1, 1),
        get_bot_sources_usecase=get_bot_sources_usecase,
        status=SourceStatus.PENDING,
        prefix="manage_sources_new",
        can_accept=True,
        can_decline=True,
        can_go_next=False,
    )


@router.callback_query(F.data.startswith("manage_sources_new_reject"))
async def manage_sources_new_reject(
    callback: CallbackQuery,
    get_bot_sources_usecase: FromDishka[GetBotSourcesUsecase],
    reject_source_usecase: FromDishka[RejectSourceUsecase],
) -> None:
    page = int(callback.data.split("_")[-1])
    bot_id = int(callback.data.split("_")[-2])

    model = (
        await get_bot_sources_usecase.execute(
            bot_id=bot_id, status=SourceStatus.PENDING, page=page
        )
    ).items[0]
    await reject_source_usecase.execute(source_id=model.id)

    await manage_sources_panel(
        callback=callback,
        bot_id=bot_id,
        page=max(page - 1, 1),
        get_bot_sources_usecase=get_bot_sources_usecase,
        status=SourceStatus.PENDING,
        prefix="manage_sources_new",
        can_accept=True,
        can_decline=True,
        can_go_next=False,
    )


@router.callback_query(F.data.startswith("manage_sources_new"))
async def manage_sources_new(
    callback: CallbackQuery, get_bot_sources_usecase: FromDishka[GetBotSourcesUsecase]
) -> None:
    page = int(callback.data.split("_")[-1])
    bot_id = int(callback.data.split("_")[-2])

    await manage_sources_panel(
        callback=callback,
        bot_id=bot_id,
        page=page,
        get_bot_sources_usecase=get_bot_sources_usecase,
        status=SourceStatus.PENDING,
        prefix="manage_sources_new",
        can_accept=True,
        can_decline=True,
        can_go_next=False,
    )


@router.callback_query(F.data.startswith("manage_sources"))
async def manage_source_screen(
    callback: CallbackQuery,
    get_bot_usecase: FromDishka[GetBotByIdUsecase],
    has_rejected_source_usecase: FromDishka[HasRejectedSourceUsecase],
    has_accepted_source_usecase: FromDishka[HasAcceptedSourceUsecase],
) -> None:
    bot_id = int(callback.data.split("_")[-1])
    bot = await get_bot_usecase.execute(bot_id=bot_id)
    has_rejected_source = await has_rejected_source_usecase.execute(bot_id=bot_id)
    has_accepted_source = await has_accepted_source_usecase.execute(bot_id=bot_id)

    if bot is None:
        await callback.message.edit_text(
            text="🥶 Бот не найден",
            reply_markup=to_menu_kb(),
        )
        return

    text = (
        f'📖 Управление источниками для бота "{bot.title.value}"\n\n'
        "Вы можете рассмотреть источники, которые используются в боте, добавить новые, если это необходимо, рассмотреть ещё раз те источники, которые были отклонены ранее.\n\n"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=manage_source_kb(
            bot_id=bot_id,
            has_declined=has_rejected_source,
            has_accepted=has_accepted_source,
        ),
    )


async def manage_sources_panel(
    callback: CallbackQuery,
    bot_id: int,
    page: int,
    get_bot_sources_usecase: GetBotSourcesUsecase,
    status: SourceStatus,
    prefix: str,
    can_decline: bool = False,
    can_accept: bool = False,
    can_go_next: bool = False,
) -> None:
    pagination = await get_bot_sources_usecase.execute(
        bot_id=bot_id, status=status, page=page
    )

    if len(pagination.items) == 0:
        await callback.message.edit_text(
            text="🏜 Источники не найдены.",
            reply_markup=retry_source_kb(path=callback.data),
        )
        return

    model = pagination.items[0]

    text = (
        f"Источник: {model.name}\n\n"
        f"Описание: {model.description}\n\n"
        f"Ссылка: {model.url}\n\n"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=change_status_source_kb(
            bot_id=bot_id,
            page=page,
            prefix=prefix,
            can_accept=can_accept,
            can_decline=can_decline,
            can_go_next=can_go_next,
            has_more=pagination.has_more,
        ),
    )
