import asyncio
from src.application.dto.summary_dto import SummaryDto
from src.di.container import init_container
from src.domain.repository.summary_repository import SummaryRepository


async def main() -> None:
    container = init_container()

    repository: SummaryRepository = await container.get(SummaryRepository)

    print(await repository.get_metrics(bot_id=1))


if __name__ == "__main__":
    asyncio.run(main())
