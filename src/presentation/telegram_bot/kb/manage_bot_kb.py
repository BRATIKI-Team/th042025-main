from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def manage_bot_kb(
    bot_id: int, page: int, is_bot_paused: bool, has_next: bool, has_previous: bool
) -> InlineKeyboardMarkup:
    kb = []

    if is_bot_paused:
        kb.append(
            [
                InlineKeyboardButton(
                    text="🟢 Включить бота", callback_data=f"resume_bot_{page}_{bot_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Удалить бота", callback_data=f"delete_bot_{page}_{bot_id}"
                ),
            ]
        )
    else:
        kb.append(
            [
                InlineKeyboardButton(
                    text="🔴 Выключить бота", callback_data=f"pause_bot_{page}_{bot_id}"
                )
            ]
        )

    kb.append(
        [
            InlineKeyboardButton(
                text="♨ Управление источниками",
                callback_data=f"manage_sources_{bot_id}",
            )
        ]
    )

    if has_next:
        kb.append(
            [
                InlineKeyboardButton(
                    text="⏩ Следующий бот", callback_data=f"manage_bot_{page + 1}"
                )
            ]
        )

    if has_previous:
        kb.append(
            [
                InlineKeyboardButton(
                    text="⏪ Предыдущий бот", callback_data=f"manage_bot_{page - 1}"
                )
            ]
        )

    kb.append([InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="menu")])

    return InlineKeyboardMarkup(inline_keyboard=kb)
