from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_kb(has_bot: bool) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Создать бота", callback_data="create_bot"),
    ]

    if has_bot:
        buttons.append(
            InlineKeyboardButton(text="Управление ботами", callback_data="manage_bot")
        )

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
