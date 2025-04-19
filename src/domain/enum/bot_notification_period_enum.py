from enum import Enum


class BotNotificationPeriod(Enum):
    MONOLITH = 10
    INSTANT = 300
    HOUR = 3600
    TWICE_A_DAY = 3600 * 12
    DAILY = 3600 * 24
