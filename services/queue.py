"""
Media processing queue.
"""

import asyncio
import logging

from services.processor import process_media
from utils.constants import MAX_QUEUE_SIZE

logger = logging.getLogger(__name__)


class MediaQueue:
    """
    Queue used to process media sequentially.
    """

    def __init__(self):

        self.queue = asyncio.Queue(
            maxsize=MAX_QUEUE_SIZE
        )

    async def add(self, job: dict):

        await self.queue.put(job)

        logger.info(
            "Queued %s | Queue Size: %s",
            job["media_type"],
            self.queue.qsize(),
        )

    async def worker(self):

        logger.info("Queue worker started.")

        while True:

            job = await self.queue.get()

            try:

                await process_media(job)

            except Exception:

                logger.exception(
                    "Error while processing job."
                )

            finally:

                self.queue.task_done()

    def size(self):

        return self.queue.qsize()


media_queue = MediaQueue()