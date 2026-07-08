"""
Media downloader service.
"""

from pathlib import Path
import logging

from aiogram import Bot

from config.settings import DOWNLOAD_DIR

logger = logging.getLogger(__name__)


async def download_media(
    bot: Bot,
    file_id: str,
    message_id: int,
) -> Path | None:
    """
    Download media from Telegram.

    Returns:
        Path to downloaded file or None.
    """

    try:

        telegram_file = await bot.get_file(file_id)

        extension = Path(
            telegram_file.file_path
        ).suffix

        filename = f"{message_id}{extension}"

        destination = DOWNLOAD_DIR / filename

        await bot.download_file(
            telegram_file.file_path,
            destination=destination,
        )

        logger.info(
            "Downloaded -> %s",
            destination,
        )

        return destination

    except Exception:

        logger.exception(
            "Download failed."
        )

        return None