import asyncio
from datetime import datetime, timedelta

from src.application.usecase.bot.get_active_bots_usecase import GetActiveBotsUsecase
from src.application.usecase.source.get_source_messages_usecase import (
    GetSourceMessagesUsecase,
)
from src.application.usecase.source.get_bot_sources_usecase import GetBotSourcesUsecase
from src.application.usecase.tg.notify_bot_usecase import NotifyBotUsecase
from src.di.container import init_container
from src.domain.enum.source_status_enum import SourceStatus


async def main() -> None:
    container = init_container()

    get_active_bots_usecase = await container.get(GetActiveBotsUsecase)
    get_bot_sources_usecase = await container.get(GetBotSourcesUsecase)
    get_source_messages_usecase = await container.get(GetSourceMessagesUsecase)
    notify_bot_usecase = await container.get(NotifyBotUsecase)

    while True:
        bots = await get_active_bots_usecase.execute()

        for bot in bots:
            start_date = datetime.now()

            sources = (
                await get_bot_sources_usecase.execute(
                    bot_id=bot.id, status=SourceStatus.ACCEPTED, page=1, page_size=9999
                )
            ).items

            at_least_one = False
            for source in sources:
                if (start_date - source.last_hit_datetime) < timedelta(
                    seconds=bot.notification_period.value
                ):
                    continue

                await get_source_messages_usecase.execute(source=source)

                at_least_one = True

            if at_least_one:
                await notify_bot_usecase.execute(bot_id=bot.id)

        await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(main())
