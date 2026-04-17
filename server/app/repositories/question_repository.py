import sqlite3
import logging

from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class QuestionRepository(BaseRepository):

    def get_or_create(self, text: str) -> int:
        try:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT id FROM questions WHERE text = ?", (text,)
                ).fetchone()
                if row:
                    return row["id"]
                cursor = conn.execute(
                    "INSERT INTO questions (text) VALUES (?)", (text,)
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error("Failed to get_or_create question: %s", e)
            raise