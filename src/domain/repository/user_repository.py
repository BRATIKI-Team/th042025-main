from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    async def ensure_user_exists(self, user_id: int) -> None:
        pass
