"""
Media uploader service.
"""

from pathlib import Path
import logging

from aiogram import Bot
from aiogram.types import (
    FSInputFile,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
)

from services.rate_limiter import rate_limiter
from services.retry import run_with_retry

logger = logging.getLogger(__name__)


async def upload_media(
    bot: Bot,
    destination_chat: int,
    media_type: str,
    file_path: Path,
    caption: str | None,
) -> bool:
    """
    Upload a single media file.
    """

    try:

        media = FSInputFile(str(file_path))

        if media_type == "photo":

            await rate_limiter.wait()

            await run_with_retry(
                bot.send_photo,
                chat_id=destination_chat,
                photo=media,
                caption=caption,
            )

        elif media_type == "video":

            await rate_limiter.wait()

            await run_with_retry(
                bot.send_video,
                chat_id=destination_chat,
                video=media,
                caption=caption,
            )

        elif media_type == "document":

            await rate_limiter.wait()

            await run_with_retry(
                bot.send_document,
                chat_id=destination_chat,
                document=media,
                caption=caption,
            )

        elif media_type == "audio":

            await rate_limiter.wait()

            await run_with_retry(
                bot.send_audio,
                chat_id=destination_chat,
                audio=media,
                caption=caption,
            )

        elif media_type == "voice":

            await rate_limiter.wait()

            await run_with_retry(
                bot.send_voice,
                chat_id=destination_chat,
                voice=media,
                caption=caption,
            )

        elif media_type == "video_note":

            await rate_limiter.wait()

            await run_with_retry(
                bot.send_video_note,
                chat_id=destination_chat,
                video_note=media,
            )

        elif media_type == "animation":

            await rate_limiter.wait()

            await run_with_retry(
                bot.send_animation,
                chat_id=destination_chat,
                animation=media,
                caption=caption,
            )

        else:

            logger.warning(
                "Unsupported media type: %s",
                media_type,
            )

            return False

        logger.info(
            "Uploaded %s -> %s",
            media_type,
            destination_chat,
        )

        return True

    except Exception:

        logger.exception(
            "Failed to upload media."
        )

        return False


async def upload_album(
    bot: Bot,
    destination_chat: int,
    files: list[dict],
) -> bool:
    """
    Upload a Telegram media album.
    """

    try:

        media_group = []

        for index, item in enumerate(files):

            media = FSInputFile(
                str(item["file_path"])
            )

            caption = (
                item["caption"]
                if index == 0
                else None
            )

            media_type = item["media_type"]

            if media_type == "photo":

                media_group.append(
                    InputMediaPhoto(
                        media=media,
                        caption=caption,
                    )
                )

            elif media_type == "video":

                media_group.append(
                    InputMediaVideo(
                        media=media,
                        caption=caption,
                    )
                )

            elif media_type == "document":

                media_group.append(
                    InputMediaDocument(
                        media=media,
                        caption=caption,
                    )
                )

            elif media_type == "audio":

                media_group.append(
                    InputMediaAudio(
                        media=media,
                        caption=caption,
                    )
                )

            else:

                logger.warning(
                    "Skipping unsupported album media: %s",
                    media_type,
                )

        if not media_group:

            logger.warning(
                "Album contains no supported media."
            )

            return False

        # Respect upload rate limit
        await rate_limiter.wait()

        # Upload the album with retry support
        await run_with_retry(
            bot.send_media_group,
            chat_id=destination_chat,
            media=media_group,
        )

        logger.info(
            "Album uploaded (%s items) -> %s",
            len(media_group),
            destination_chat,
        )

        return True

    except Exception:

        logger.exception(
            "Failed to upload album."
        )

        return False