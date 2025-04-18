from enum import Enum


class BotNotificationPeriod(Enum):
    INSTANT = 0
    HOUR = 1
    TWICE_A_DAY = 2
    DAILY = 3
