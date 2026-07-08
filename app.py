"""
Application entry point for Telegram Media Mirror.
"""

from __future__ import annotations

import asyncio
import logging

from bot.client import bot, dp
from bot.commands import router as command_router
from bot.handlers import router as media_router
from config.logging_config import setup_logging
from database.database import database
from services.queue import media_queue

# Configure logging
setup_logging()

logger = logging.getLogger(__name__)


async def startup() -> None:
    """
    Initialize application resources.
    """

    logger.info("=" * 60)
    logger.info("Telegram Media Mirror")
    logger.info("Starting application...")
    logger.info("=" * 60)

    # Initialize database
    await database.initialize()
    logger.info("Database initialized.")

    # Register routers
    dp.include_router(command_router)
    dp.include_router(media_router)
    logger.info("Routers registered.")

    # Start background queue worker
    asyncio.create_task(media_queue.worker())
    logger.info("Queue worker started.")

    logger.info("Bot started.")
    logger.info("Start polling...")


async def shutdown() -> None:
    """
    Cleanup before shutting down.
    """

    logger.info("Stopping application...")


async def main() -> None:
    """
    Main application entry point.
    """

    await startup()

    try:
        await dp.start_polling(bot)

    finally:
        await shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("Application stopped by user.")

    except Exception:
        logger.exception("Unexpected application error.")