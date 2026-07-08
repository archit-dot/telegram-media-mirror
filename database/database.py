"""
SQLite database service.
"""

from __future__ import annotations

import aiosqlite

from config.settings import DATABASE


class Database:
    """
    Database service for mirror mappings.
    """

    def __init__(self) -> None:
        self.database = DATABASE

    async def initialize(self) -> None:

        async with aiosqlite.connect(self.database) as db:

            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS mirrors (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    source_chat_id INTEGER NOT NULL,

                    destination_chat_id INTEGER NOT NULL,

                    enabled INTEGER NOT NULL DEFAULT 1,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    UNIQUE(source_chat_id, destination_chat_id)

                );
                """
            )

            await db.commit()

    async def add_mirror(
        self,
        source_chat_id: int,
        destination_chat_id: int,
    ) -> bool:

        async with aiosqlite.connect(self.database) as db:

            try:

                await db.execute(
                    """
                    INSERT INTO mirrors(
                        source_chat_id,
                        destination_chat_id
                    )
                    VALUES (?,?)
                    """,
                    (
                        source_chat_id,
                        destination_chat_id,
                    ),
                )

                await db.commit()

                return True

            except aiosqlite.IntegrityError:

                return False

    async def remove_mirror(
        self,
        source_chat_id: int,
        destination_chat_id: int,
    ) -> bool:

        async with aiosqlite.connect(self.database) as db:

            cursor = await db.execute(
                """
                DELETE FROM mirrors

                WHERE source_chat_id = ?

                AND destination_chat_id = ?
                """,
                (
                    source_chat_id,
                    destination_chat_id,
                ),
            )

            await db.commit()

            return cursor.rowcount > 0

    async def get_destinations(
        self,
        source_chat_id: int,
    ) -> list[int]:

        async with aiosqlite.connect(self.database) as db:

            cursor = await db.execute(
                """
                SELECT destination_chat_id

                FROM mirrors

                WHERE source_chat_id = ?

                AND enabled = 1
                """,
                (
                    source_chat_id,
                ),
            )

            rows = await cursor.fetchall()

            return [row[0] for row in rows]

    async def list_mirrors(self) -> list[tuple]:

        async with aiosqlite.connect(self.database) as db:

            cursor = await db.execute(
                """
                SELECT

                    source_chat_id,

                    destination_chat_id

                FROM mirrors

                ORDER BY id ASC
                """
            )

            return await cursor.fetchall()

    async def count_mirrors(self) -> int:

        async with aiosqlite.connect(self.database) as db:

            cursor = await db.execute(
                """
                SELECT COUNT(*)

                FROM mirrors
                """
            )

            row = await cursor.fetchone()

            return row[0]

    async def mirror_exists(
        self,
        source_chat_id: int,
        destination_chat_id: int,
    ) -> bool:

        async with aiosqlite.connect(self.database) as db:

            cursor = await db.execute(
                """
                SELECT id

                FROM mirrors

                WHERE source_chat_id = ?

                AND destination_chat_id = ?

                LIMIT 1
                """,
                (
                    source_chat_id,
                    destination_chat_id,
                ),
            )

            return await cursor.fetchone() is not None


database = Database()