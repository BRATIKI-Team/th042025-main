from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.domain.enum.bot_notification_period_enum import BotNotificationPeriod


def bot_notification_period_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔔 МОНОЛИТ", callback_data=BotNotificationPeriod.MONOLITH
                ),
                InlineKeyboardButton(
                    text="🔔 Мгновенно", callback_data=BotNotificationPeriod.MONOLITH
                ),
                InlineKeyboardButton(
                    text="⏰ 1 час", callback_data=BotNotificationPeriod.HOUR
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⏳ 12 часов", callback_data=BotNotificationPeriod.TWICE_A_DAY
                ),
                InlineKeyboardButton(
                    text="⌛ 24 часа", callback_data=BotNotificationPeriod.DAILY
                ),
            ],
        ]
    )
