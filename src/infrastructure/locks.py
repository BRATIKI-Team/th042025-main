import asyncio
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class LockManager:
    """
    Singleton class for managing locks across the application.
    """
    _instance: Optional['LockManager'] = None
    _locks: Dict[str, asyncio.Lock] = {}
    _semaphores: Dict[str, asyncio.Semaphore] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LockManager, cls).__new__(cls)
        return cls._instance

    def get_lock(self, key: str) -> asyncio.Lock:
        """
        Get or create a lock for the given key.
        """
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    def get_semaphore(self, key: str, value: int = 1) -> asyncio.Semaphore:
        """
        Get or create a semaphore for the given key.
        """
        if key not in self._semaphores:
            self._semaphores[key] = asyncio.Semaphore(value)
        return self._semaphores[key] 