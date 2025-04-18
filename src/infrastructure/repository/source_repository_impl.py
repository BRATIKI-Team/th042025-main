from src.domain.enum.source_status_enum import SourceStatus
from src.domain.model.source_model import SourceModel
from src.domain.repository.source_repository import SourceRepository
from src.infrastructure.dao.source_dao import SourceDAO


class SourceRepositoryImpl(SourceRepository):
    async def get_source_by_status(self, status: SourceStatus) -> SourceModel | None:
        dao = await SourceDAO.objects().get(SourceDAO.status == status.value).first()

        if dao is None:
            return None

        return SourceDAO.from_dao(dao)
