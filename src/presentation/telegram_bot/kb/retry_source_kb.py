from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def retry_source_kb(path: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Повторить поиск", callback_data=path)],
            [
                InlineKeyboardButton(
                    text="⏪ Вернуться к ботам", callback_data="manage_bot"
                )
            ],
        ]
    )
