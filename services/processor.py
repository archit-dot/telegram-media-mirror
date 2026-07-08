"""
Media processor.
"""

from pathlib import Path
import logging

from bot.client import bot
from database.database import database
from services.downloader import download_media
from services.uploader import (
    upload_album,
    upload_media,
)

logger = logging.getLogger(__name__)


async def process_media(job: dict) -> None:
    """
    Process queued media.
    """

    # -----------------------------------------
    # Album
    # -----------------------------------------

    if job.get("album"):

        await process_album(job)

        return

    # -----------------------------------------
    # Single Media
    # -----------------------------------------

    file_path = await download_media(
        bot=bot,
        file_id=job["file_id"],
        message_id=job["message_id"],
    )

    if file_path is None:
        return

    destinations = await database.get_destinations(
        job["chat_id"]
    )

    if not destinations:

        logger.info(
            "No destination configured."
        )

        try:
            file_path.unlink()
        except Exception:
            pass

        return

    for destination in destinations:

        await upload_media(
            bot=bot,
            destination_chat=destination,
            media_type=job["media_type"],
            file_path=file_path,
            caption=job["caption"],
        )

    try:

        file_path.unlink()

    except Exception:

        logger.exception(
            "Unable to delete file."
        )


async def process_album(job: dict) -> None:
    """
    Download every file of an album.
    """

    items = job["items"]

    downloaded_files: list[dict] = []

    first = items[0]

    for item in items:

        file_path = await download_media(
            bot=bot,
            file_id=item["file_id"],
            message_id=item["message_id"],
        )

        if file_path is None:
            continue

        downloaded_files.append(
            {
                "media_type": item["media_type"],
                "file_path": file_path,
                "caption": item["caption"],
            }
        )

    if not downloaded_files:

        return

    destinations = await database.get_destinations(
        first["chat_id"]
    )

    if not destinations:

        for media in downloaded_files:

            try:
                media["file_path"].unlink()
            except Exception:
                pass

        return

    for destination in destinations:

        await upload_album(
            bot=bot,
            destination_chat=destination,
            files=downloaded_files,
        )

    for media in downloaded_files:

        try:

            media["file_path"].unlink()

        except Exception:

            logger.exception(
                "Unable to delete album file."
            )