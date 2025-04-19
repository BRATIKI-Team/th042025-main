from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def change_status_source_kb(
    bot_id: int,
    page: int,
    prefix: str,
    can_accept: bool,
    can_decline: bool,
    can_go_next: bool,
    has_more: bool,
) -> InlineKeyboardMarkup:
    kb = []

    if can_accept:
        kb.append(
            [
                InlineKeyboardButton(
                    text="✅ Принять", callback_data=f"{prefix}_accept_{bot_id}_{page}"
                )
            ]
        )

    if can_decline:
        kb.append(
            [
                InlineKeyboardButton(
                    text="❌ Отклонить", callback_data=f"{prefix}_reject_{bot_id}_{page}"
                )
            ]
        )

    if can_go_next and has_more:
        kb.append(
            [
                InlineKeyboardButton(
                    text="⏩ Следующий", callback_data=f"{prefix}_{bot_id}_{page + 1}"
                )
            ]
        )

    if page != 1:
        kb.append(
            [
                InlineKeyboardButton(
                    text="⏪ Предыдущий",
                    callback_data=f"{prefix}_{bot_id}_{max(page - 1, 1)}",
                )
            ]
        )

    kb.append(
        [InlineKeyboardButton(text="🏡 Вернуться к ботам", callback_data=f"manage_bot")]
    )

    return InlineKeyboardMarkup(inline_keyboard=kb)
