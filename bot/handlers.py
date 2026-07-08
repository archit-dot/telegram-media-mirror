"""
Media handlers.
"""

import asyncio
import logging

from aiogram import Router
from aiogram.types import Message

from services.queue import media_queue

logger = logging.getLogger(__name__)

router = Router()

# Temporary storage for albums
albums = {}


@router.message()
async def media_handler(message: Message) -> None:
    """
    Detect supported media.
    """

    media_type = None
    file_id = None

    if message.photo:
        media_type = "photo"
        file_id = message.photo[-1].file_id

    elif message.video:
        media_type = "video"
        file_id = message.video.file_id

    elif message.document:
        media_type = "document"
        file_id = message.document.file_id

    elif message.audio:
        media_type = "audio"
        file_id = message.audio.file_id

    elif message.voice:
        media_type = "voice"
        file_id = message.voice.file_id

    elif message.video_note:
        media_type = "video_note"
        file_id = message.video_note.file_id

    elif message.animation:
        media_type = "animation"
        file_id = message.animation.file_id

    else:
        return

    # -----------------------------
    # Album Support
    # -----------------------------

    if message.media_group_id:

        album_id = message.media_group_id

        if album_id not in albums:

            albums[album_id] = []

            asyncio.create_task(
                process_album(
                    album_id
                )
            )

        albums[album_id].append(
            {
                "chat_id": message.chat.id,
                "message_id": message.message_id,
                "media_type": media_type,
                "file_id": file_id,
                "caption": message.caption,
            }
        )

        return

    # -----------------------------
    # Single Media
    # -----------------------------

    job = {
        "chat_id": message.chat.id,
        "message_id": message.message_id,
        "media_type": media_type,
        "file_id": file_id,
        "caption": message.caption,
        "album": False,
    }

    await media_queue.add(job)

    logger.info(
        "Queued %s",
        media_type,
    )


async def process_album(
    album_id: str,
) -> None:
    """
    Wait briefly to collect
    all messages belonging
    to the same album.
    """

    await asyncio.sleep(1)

    messages = albums.pop(
        album_id,
        [],
    )

    if not messages:
        return

    await media_queue.add(
        {
            "album": True,
            "items": messages,
        }
    )

    logger.info(
        "Queued Album (%s items)",
        len(messages),
    )