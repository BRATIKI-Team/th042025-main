from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_sources_kb(is_refreshing: bool = False) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перейти к выбору источников"
                    if not is_refreshing
                    else "Обновить список источников",
                    callback_data="select_sources",
                )
            ],
        ]
    )
