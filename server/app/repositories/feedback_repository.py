import sqlite3
import logging

from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class FeedbackRepository(BaseRepository):

    def save(self, question_id: int, rating: int, comment: str | None = None) -> None:
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO feedback (question_id, rating, comment)
                    VALUES (?, ?, ?)
                    """,
                    (question_id, rating, comment),
                )
        except sqlite3.Error as e:
            logger.error("Failed to save feedback: %s", e)
            raise

    def list(self, page: int = 1, limit: int = 20) -> list[dict]:
        offset = (page - 1) * limit
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT
                        f.id,
                        q.text AS question,
                        f.rating,
                        f.comment,
                        f.created_at
                    FROM feedback f
                    JOIN questions q ON q.id = f.question_id
                    ORDER BY f.created_at DESC
                    LIMIT ? OFFSET ?
                    """,
                    (limit, offset),
                ).fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error("Failed to list feedback: %s", e)
            return []

    def count(self) -> int:
        try:
            with self._connect() as conn:
                return conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
        except sqlite3.Error:
            return 0