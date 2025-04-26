import asyncio
import time
from typing import Optional
import logging


class RateLimiter:
    """
    A rate limiter that uses semaphores to control the rate of operations.
    This is useful for preventing rate limit errors (like 429) by controlling
    the number of concurrent requests.
    """

    def __init__(
        self,
        max_concurrent: int = 1,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the rate limiter.

        Args:
            max_concurrent: Maximum number of concurrent operations allowed
            logger: Optional logger instance
        """
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._logger = logger or logging.getLogger(__name__)

    async def acquire(self):
        """
        Acquire a permit to perform an operation.
        This will block if the maximum number of concurrent operations is reached.
        """
        self._logger.info(
            "---Acquiring semaphore: max_concurrent=%d", self._semaphore._value
        )
        await self._semaphore.acquire()
        self._logger.info(
            "---Finished acquiring semaphore: max_concurrent=%d", self._semaphore._value
        )

    def release(self):
        """
        Release a permit after an operation is completed.
        """
        self._logger.info(
            "---Releasing semaphore: max_concurrent=%d", self._semaphore._value
        )
        self._semaphore.release()

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()


def rate_limit(
    max_concurrent: int = 1,
    logger: Optional[logging.Logger] = None,
):
    """
    Decorator for implementing rate limiting using semaphores.

    Args:
        max_concurrent: Maximum number of concurrent operations allowed
        logger: Optional logger instance
    """
    limiter = RateLimiter(max_concurrent, logger)

    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with limiter:
                return await func(*args, **kwargs)

        return wrapper

    return decorator
