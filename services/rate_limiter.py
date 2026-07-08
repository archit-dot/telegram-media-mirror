"""
Rate limiter service.
"""

import asyncio
import logging

from config.settings import RATE_LIMIT_PER_MINUTE

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Controls upload speed.
    """

    def __init__(self) -> None:

        self.delay = 60 / RATE_LIMIT_PER_MINUTE

        logger.info(
            "Rate limiter: %.2f sec/upload",
            self.delay,
        )

    async def wait(self) -> None:

        await asyncio.sleep(self.delay)


rate_limiter = RateLimiter()