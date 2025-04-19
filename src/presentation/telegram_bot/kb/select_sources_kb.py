from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_sources_kb(
    text: str = "Перейти к выбору источников", can_stop_searching: bool = False
) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text=text,
                callback_data="select_sources",
            )
        ]
    ]

    if can_stop_searching:
        kb.append(
            [InlineKeyboardButton(text="🛑 Остановить поиск", callback_data="menu_new")]
        )

    return InlineKeyboardMarkup(inline_keyboard=kb)
