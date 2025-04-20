import asyncio
import logging
import signal
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Set

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.job import Job

from src.di.container import init_container
from src.application.usecase.get_grouped_sources_usecase import GetGroupedSourcesUsecase
from src.application.usecase.get_source_messages_usecase import GetSourceMessagesUsecase
from src.application.usecase.notify_bot_usecase import NotifyBotUsecase
from src.domain.model.grouped_source_model import GroupedSourceModel


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

# Global variables for source management
active_jobs: Dict[str, Job] = {}  # Maps job_id to Job object
source_polling_interval = 60  # Poll for new sources every 60 seconds


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
        try:
            await get_source_messages_usecase.execute(grouped_source)
            logger.info(f"Successfully processed source group: {grouped_source.url}")
        except asyncio.CancelledError:
            logger.warning(f"Source group processing was cancelled: {grouped_source.url}")
            return
        except Exception as e:
            logger.error(f"Error getting messages for source group {grouped_source.url}: {str(e)}")
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
        for bot_id in bots_to_notify:
            try:
                logger.info(f"Notifying bot {bot_id} messages from sources")
                await notify_bot_usecase.execute(bot_id)
            except asyncio.CancelledError:
                logger.warning(f"Bot notification was cancelled for bot {bot_id}")
                return
            except Exception as e:
                logger.error(f"Error notifying bot {bot_id}: {str(e)}")

    except Exception as e:
        logger.error(f"Error processing source group {grouped_source.url}: {str(e)}")


def create_job_id(period: int, source_url: str) -> str:
    """
    Create a unique job ID for a source group.
    """
    return f"process_sources_period_{period}_{source_url}"


def update_scheduler_jobs(
    scheduler: AsyncIOScheduler,
    grouped_sources: List[GroupedSourceModel],
    get_source_messages_usecase,
    notify_bot_usecase,
) -> None:
    """
    Update scheduler jobs based on current grouped sources.
    """
    # Get current active job IDs
    current_job_ids = set(active_jobs.keys())
    
    # Create a set of required job IDs based on current sources
    required_job_ids = set()
    for source in grouped_sources:
        job_id = create_job_id(source.notification_period, source.url)
        required_job_ids.add(job_id)
        
        # If this is a new job, add it to the scheduler
        if job_id not in current_job_ids:
            logger.info(f"Adding new job for source {source.url} with period {source.notification_period}")
            job = scheduler.add_job(
                process_sources_for_period,
                IntervalTrigger(seconds=source.notification_period),
                args=[[source], get_source_messages_usecase, notify_bot_usecase],
                id=job_id,
                replace_existing=True,
            )
            active_jobs[job_id] = job
    
    # Remove jobs that are no longer needed
    jobs_to_remove = current_job_ids - required_job_ids
    for job_id in jobs_to_remove:
        logger.info(f"Removing obsolete job {job_id}")
        scheduler.remove_job(job_id)
        del active_jobs[job_id]


async def poll_sources(
    scheduler: AsyncIOScheduler,
    get_grouped_sources_usecase,
    get_source_messages_usecase,
    notify_bot_usecase,
) -> None:
    """
    Poll for new sources and update scheduler jobs.
    """
    while not shutdown_event.is_set():
        try:
            # Get current grouped sources
            grouped_sources = await get_grouped_sources_usecase.execute()
            
            # Update scheduler jobs
            update_scheduler_jobs(
                scheduler,
                grouped_sources,
                get_source_messages_usecase,
                notify_bot_usecase,
            )
            
            # Wait for next polling interval
            await asyncio.sleep(source_polling_interval)
            
        except asyncio.CancelledError:
            logger.info("Source polling was cancelled")
            break
        except Exception as e:
            logger.error(f"Error polling sources: {str(e)}")
            await asyncio.sleep(source_polling_interval)


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

    # Get initial grouped sources and set up jobs
    grouped_sources = await get_grouped_sources_usecase.execute()
    update_scheduler_jobs(
        scheduler,
        grouped_sources,
        get_source_messages_usecase,
        notify_bot_usecase,
    )

    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started")

    # Start source polling task
    polling_task = asyncio.create_task(
        poll_sources(
            scheduler,
            get_grouped_sources_usecase,
            get_source_messages_usecase,
            notify_bot_usecase,
        )
    )

    # Keep the script running until shutdown event is set
    try:
        await shutdown_event.wait()
    except asyncio.CancelledError:
        logger.info("Scheduler task was cancelled")
    finally:
        if not force_exit:
            # Cancel polling task
            polling_task.cancel()
            try:
                await polling_task
            except asyncio.CancelledError:
                pass
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
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.warning("Source processing was cancelled")
        except Exception as e:
            logger.error(f"Error processing sources: {str(e)}")


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
