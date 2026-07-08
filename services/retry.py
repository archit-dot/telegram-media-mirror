"""
Retry service for uploads.
"""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.exceptions import TelegramRetryAfter

from config.settings import MAX_RETRIES

logger = logging.getLogger(__name__)


async def run_with_retry(
    operation: Callable[..., Awaitable[Any]],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Execute an async operation with retry support.
    """

    attempt = 0

    while attempt < MAX_RETRIES:

        try:

            return await operation(
                *args,
                **kwargs,
            )

        except TelegramRetryAfter as error:

            wait_time = error.retry_after

            logger.warning(
                "FloodWait detected. Sleeping %.2f seconds.",
                wait_time,
            )

            await asyncio.sleep(wait_time)

        except Exception as error:

            attempt += 1

            logger.warning(
                "Retry %s/%s : %s",
                attempt,
                MAX_RETRIES,
                error,
            )

            if attempt >= MAX_RETRIES:

                logger.exception(
                    "Maximum retries reached."
                )

                raise

            await asyncio.sleep(2)