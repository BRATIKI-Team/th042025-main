from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def manage_source_kb(
    bot_id: int, has_declined: bool, has_accepted: bool
) -> InlineKeyboardMarkup:
    kb = []

    if has_accepted:
        kb.append(
            [
                InlineKeyboardButton(
                    text="💞 Показать принятые источники",
                    callback_data=f"manage_sources_accepted_{bot_id}_1",
                )
            ]
        )
    kb.append(
        [
            InlineKeyboardButton(
                text="🆕 Поиск новых источников",
                callback_data=f"manage_sources_new_{bot_id}_1",
            )
        ]
    )
    if has_declined:
        kb.append(
            [
                InlineKeyboardButton(
                    text="😾 Показать отклоненные источники",
                    callback_data=f"manage_sources_declined_{bot_id}_1",
                )
            ]
        )
    kb.append(
        [InlineKeyboardButton(text="⏪ Вернуться к ботам", callback_data=f"manage_bot")]
    )

    return InlineKeyboardMarkup(inline_keyboard=kb)
