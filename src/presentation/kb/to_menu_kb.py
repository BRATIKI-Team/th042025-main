from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def to_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="menu")]
        ]
    )
