from abc import ABC, abstractmethod


class BotRepository(ABC):
    @abstractmethod
    async def has_bot(self, user_id: int) -> bool:
        pass
