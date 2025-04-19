from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def source_kb(source_id: int, can_stop_searching: bool = False) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="✅ Принять", callback_data=f"accept_source_{source_id}   "
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отклонить", callback_data=f"reject_source_{source_id}"
            )
        ],
    ]

    if can_stop_searching:
        kb.append(
            [InlineKeyboardButton(text="🛑 Остановить поиск", callback_data="menu")]
        )

    return InlineKeyboardMarkup(inline_keyboard=kb)
