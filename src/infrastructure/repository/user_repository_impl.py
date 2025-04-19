from src.domain.repository.user_repository import UserRepository
from src.infrastructure.dao.user_dao import UserDAO


class UserRepositoryImpl(UserRepository):
    async def ensure_user_exists(self, user_id: int) -> None:
        dao = await UserDAO.objects().get(UserDAO.id == user_id).first()

        if dao is None:
            await UserDAO.objects().create(id=user_id)
