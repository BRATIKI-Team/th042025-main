from src.application.dto.source_response import SourceResponse
from src.domain.model.source_model import SourceModel


class SourceMapper:
    @staticmethod
    def to_response(source: SourceModel) -> SourceResponse:
        return SourceResponse(
            id=source.id,
            name=source.name,
            description=source.description,
            type=source.type.value,
            url=source.url,
        )
