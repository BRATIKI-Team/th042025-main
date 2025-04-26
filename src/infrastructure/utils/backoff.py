import asyncio
import functools
import logging
from typing import Type, Optional
from datetime import datetime


def backoff(
    exception: Type[Exception],
    max_tries: int = 20,
    max_time: int = 120,  # seconds
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    logger: Optional[logging.Logger] = None,
):
    """
    Decorator for implementing exponential backoff for async functions.

    Args:
        exception: Single exception type to catch
        max_tries: Maximum number of retries
        max_time: Maximum time in seconds to retry
        initial_delay: Initial delay between retries in seconds
        exponential_base: Base for exponential backoff
        logger: Optional logger instance
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = datetime.now()
            delay = initial_delay
            tries = 0

            while True:
                try:
                    return await func(*args, **kwargs)
                except exception as e:
                    tries += 1
                    elapsed_time = (datetime.now() - start_time).total_seconds()

                    if tries >= max_tries or elapsed_time >= max_time:
                        logger.error(
                            f"Max retries ({max_tries}) or time ({max_time}s) exceeded for {func.__name__}. "
                            f"Last error: {str(e)}"
                        )
                        raise

                    # Calculate next delay with exponential backoff
                    delay = min(
                        initial_delay * (exponential_base ** (tries - 1)),
                        max_time - elapsed_time,
                    )

                    logger.warning(
                        f"Retrying {func.__name__} after {delay:.2f}s (attempt {tries}/{max_tries}). "
                        f"Error: {str(e)}"
                    )

                    await asyncio.sleep(delay)

        return wrapper

    return decorator
