from abc import ABC, abstractmethod


class BotUserRepository(ABC):
    @abstractmethod
    async def create_bot_user(self, bot_id: int, user_id: int) -> None:
        pass

    @abstractmethod
    async def get_users_count(self, bot_id: int) -> int:
        pass
