"""
Bot command handlers.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.settings import OWNER_ID
from database.database import database
from services.queue import media_queue
from utils.helpers import pending_links, pending_unlinks

router = Router()


def is_owner(message: Message) -> bool:
    """
    Returns True if the sender is the bot owner.
    """

    return (
        message.from_user is not None
        and message.from_user.id == OWNER_ID
    )


# ==========================================================
# START
# ==========================================================

@router.message(Command("start"))
async def start_command(message: Message) -> None:

    await message.answer(
        "✅ Telegram Media Mirror is running."
    )


# ==========================================================
# HELP
# ==========================================================

@router.message(Command("help"))
async def help_command(message: Message) -> None:

    text = (
        "📖 Available Commands\n\n"
        "/start\n"
        "/help\n\n"
        "/status\n"
        "/list\n\n"
        "/link\n"
        "/finishlink\n\n"
        "/unlink\n"
        "/finishunlink"
    )

    await message.answer(text)


# ==========================================================
# STATUS
# ==========================================================

@router.message(Command("status"))
async def status_command(message: Message) -> None:

    if not is_owner(message):
        return

    mirror_count = await database.count_mirrors()

    text = (
        "🤖 Telegram Media Mirror\n\n"
        "🟢 Status      : Online\n"
        f"📦 Mirrors     : {mirror_count}\n"
        f"📬 Queue Size  : {media_queue.size()}\n"
        "🗄 Database    : Connected"
    )

    await message.answer(text)


# ==========================================================
# LIST
# ==========================================================

@router.message(Command("list"))
async def list_command(message: Message) -> None:

    if not is_owner(message):
        return

    mirrors = await database.list_mirrors()

    if not mirrors:

        await message.answer(
            "No mirrors configured."
        )

        return

    text = "📋 Configured Mirrors\n\n"

    for index, mirror in enumerate(
        mirrors,
        start=1,
    ):

        source_id = mirror[0]

        destination_id = mirror[1]

        try:

            source_chat = await message.bot.get_chat(
                source_id
            )

            source_name = source_chat.title

        except Exception:

            source_name = str(source_id)

        try:

            destination_chat = await message.bot.get_chat(
                destination_id
            )

            destination_name = destination_chat.title

        except Exception:

            destination_name = str(destination_id)

        text += (
            f"{index}.\n"
            f"📥 Source      : {source_name}\n"
            f"📤 Destination : {destination_name}\n\n"
        )

    await message.answer(text)


# ==========================================================
# LINK
# ==========================================================

@router.message(Command("link"))
async def link_command(message: Message) -> None:

    if not is_owner(message):
        return

    pending_links[OWNER_ID] = message.chat.id

    await message.answer(
        "✅ Source group selected.\n\n"
        "Now go to the destination group "
        "and run /finishlink."
    )


@router.message(Command("finishlink"))
async def finish_link_command(message: Message) -> None:

    if not is_owner(message):
        return

    if OWNER_ID not in pending_links:

        await message.answer(
            "❌ Run /link in the source group first."
        )

        return

    source = pending_links[OWNER_ID]

    destination = message.chat.id

    if source == destination:

        await message.answer(
            "❌ Source and destination cannot be the same."
        )

        pending_links.pop(
            OWNER_ID,
            None,
        )

        return

    try:

        bot_user = await message.bot.get_me()

        await message.bot.get_chat_member(
            source,
            bot_user.id,
        )

        await message.bot.get_chat_member(
            destination,
            bot_user.id,
        )

    except Exception:

        await message.answer(
            "❌ Unable to verify bot permissions."
        )

        return

    success = await database.add_mirror(
        source,
        destination,
    )

    pending_links.pop(
        OWNER_ID,
        None,
    )

    if success:

        try:

            source_chat = await message.bot.get_chat(
                source
            )

            destination_chat = await message.bot.get_chat(
                destination
            )

            source_name = source_chat.title

            destination_name = destination_chat.title

        except Exception:

            source_name = str(source)

            destination_name = str(destination)

        await message.answer(
            f"✅ Mirror Created\n\n"
            f"📥 {source_name}\n"
            f"⬇️\n"
            f"📤 {destination_name}"
        )

    else:

        await message.answer(
            "Mirror already exists."
        )


# ==========================================================
# UNLINK
# ==========================================================

@router.message(Command("unlink"))
async def unlink_command(message: Message) -> None:

    if not is_owner(message):
        return

    pending_unlinks[OWNER_ID] = message.chat.id

    await message.answer(
        "✅ Source selected.\n\n"
        "Now go to the destination group "
        "and run /finishunlink."
    )


@router.message(Command("finishunlink"))
async def finish_unlink_command(message: Message) -> None:

    if not is_owner(message):
        return

    if OWNER_ID not in pending_unlinks:

        await message.answer(
            "❌ Run /unlink in the source group first."
        )

        return

    source = pending_unlinks[OWNER_ID]

    destination = message.chat.id

    success = await database.remove_mirror(
        source,
        destination,
    )

    pending_unlinks.pop(
        OWNER_ID,
        None,
    )

    if success:

        await message.answer(
            "✅ Mirror removed successfully."
        )

    else:

        await message.answer(
            "Mirror not found."
        )