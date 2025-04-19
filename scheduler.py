import asyncio
import logging
import signal
import sys
import time
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.di.container import init_container
from src.application.usecase.get_grouped_sources_usecase import GetGroupedSourcesUsecase
from src.application.usecase.get_source_messages_usecase import GetSourceMessagesUsecase
from src.application.usecase.notify_bot_usecase import NotifyBotUsecase


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Global variables for graceful shutdown
scheduler = None
shutdown_event = None
force_exit = False
last_signal_time = 0


async def process_source_group(
    grouped_source, get_source_messages_usecase, notify_bot_usecase
):
    """
    Process a group of sources with the same type and URL.
    """
    try:
        logger.info(
            f"Processing source group: {grouped_source.url} (type: {grouped_source.type})"
        )
        messages = await get_source_messages_usecase.execute(grouped_source)
        logger.info(f"Successfully processed source group: {grouped_source.url}")

        if len(messages) == 0:
            return

        now = datetime.now()
        bots_to_notify = []
        # Get bots for each source in the group
        for source in grouped_source.sources:

            # Get bots associated with this source
            if source.bot_last_notified_at is None or (
                now - source.bot_last_notified_at
            ) >= timedelta(seconds=source.bot_notification_period):
                bots_to_notify.append(source.bot_id)

        # Notify each bot
        for bot in bots_to_notify:
            logger.info(
                f"Notifying bot {bot} about {len(messages)} messages from sources"
            )
            await notify_bot_usecase.execute(bot, messages)

    except Exception as e:
        logger.error(f"Error processing source group {grouped_source.url}: {str(e)}")
        raise e


async def setup_scheduler():
    """
    Set up the scheduler with jobs for each notification period.
    """
    global scheduler, shutdown_event

    # Initialize shutdown event
    shutdown_event = asyncio.Event()

    # Initialize DI container
    container = init_container()

    # Get usecases from container
    get_grouped_sources_usecase = await container.get(GetGroupedSourcesUsecase)
    get_source_messages_usecase = await container.get(GetSourceMessagesUsecase)
    notify_bot_usecase = await container.get(NotifyBotUsecase)

    # Create scheduler
    scheduler = AsyncIOScheduler()

    # Get grouped sources
    grouped_sources = await get_grouped_sources_usecase.execute()

    # Group sources by notification period
    notification_periods = {}
    for source in grouped_sources:
        period = source.notification_period
        if period not in notification_periods:
            notification_periods[period] = []
        notification_periods[period].append(source)

    # Create jobs for each notification period
    for period, sources in notification_periods.items():
        # Convert period to seconds (assuming period is in minutes)
        interval_seconds = period

        # Create a job for this notification period
        scheduler.add_job(
            process_sources_for_period,
            IntervalTrigger(seconds=interval_seconds),
            args=[sources, get_source_messages_usecase, notify_bot_usecase],
            id=f"process_sources_period_{period}",
            replace_existing=True,
        )

        logger.info(
            f"Added job for notification period {period} minutes with {len(sources)} source groups"
        )

    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started")

    # Keep the script running until shutdown event is set
    try:
        await shutdown_event.wait()
    except asyncio.CancelledError:
        logger.info("Scheduler task was cancelled")
    finally:
        if not force_exit:
            await graceful_shutdown()


async def process_sources_for_period(
    sources, get_source_messages_usecase, notify_bot_usecase
):
    """
    Process all sources for a specific notification period.
    """
    tasks = []
    for source in sources:
        # Check if it's time to process this source
        time_since_last_hit = datetime.now() - source.last_hit_datetime
        if time_since_last_hit >= timedelta(seconds=source.notification_period):
            tasks.append(
                process_source_group(
                    source, get_source_messages_usecase, notify_bot_usecase
                )
            )

    if tasks:
        await asyncio.gather(*tasks)


async def graceful_shutdown():
    """
    Gracefully shut down the scheduler and wait for running jobs to complete.
    """
    global scheduler

    if scheduler:
        logger.info("Shutting down scheduler...")

        # Shutdown the scheduler
        scheduler.shutdown(wait=True)

        # Wait for any running jobs to complete
        running_jobs = scheduler.get_jobs()
        if running_jobs:
            logger.info(f"Waiting for {len(running_jobs)} running jobs to complete...")
            for job in running_jobs:
                if job.next_run_time:
                    logger.info(f"Job {job.id} will complete at {job.next_run_time}")

        logger.info("Scheduler shut down successfully")


def handle_shutdown(signum, frame):
    """
    Handle shutdown signals (SIGINT, SIGTERM).
    First Ctrl+C initiates graceful shutdown, second Ctrl+C forces immediate exit.
    """
    global force_exit, last_signal_time

    current_time = time.time()

    # Check if this is a second Ctrl+C within 3 seconds
    if current_time - last_signal_time < 3:
        logger.warning("Second Ctrl+C received. Forcing immediate exit!")
        force_exit = True
        sys.exit(1)

    # Record the time of this signal
    last_signal_time = current_time

    logger.info(f"Received signal {signum}. Initiating graceful shutdown...")
    logger.info("Press Ctrl+C again within 3 seconds to force immediate exit.")

    # Set the shutdown event to signal the main loop to exit
    if shutdown_event:
        shutdown_event.set()
    else:
        # If the event doesn't exist yet, exit immediately
        sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    # Run the scheduler
    asyncio.run(setup_scheduler())
