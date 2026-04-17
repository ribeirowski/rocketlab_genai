import sqlite3
import logging

from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class HistoryRepository(BaseRepository):

    def save(
        self,
        question_id: int,
        generated_sql: str,
        row_count: int,
        success: bool = True,
        analysis: str | None = None,
        error: str | None = None,
    ) -> None:
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO query_history (question_id, generated_sql, row_count, success, analysis, error)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (question_id, generated_sql, row_count, success, analysis, error),
                )
        except sqlite3.Error as e:
            logger.warning("Failed to save history: %s", e)

    def list(self, page: int = 1, limit: int = 20) -> list[dict]:
        offset = (page - 1) * limit
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT
                        h.id,
                        q.text AS question,
                        h.generated_sql,
                        h.analysis,
                        h.row_count,
                        h.success,
                        h.error,
                        f.rating,
                        f.comment,
                        h.created_at
                    FROM query_history h
                    JOIN questions q ON q.id = h.question_id
                    LEFT JOIN feedback f ON f.question_id = h.question_id
                    ORDER BY h.created_at DESC
                    LIMIT ? OFFSET ?
                    """,
                    (limit, offset),
                ).fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error("Failed to list history: %s", e)
            return []

    def count(self) -> int:
        try:
            with self._connect() as conn:
                return conn.execute("SELECT COUNT(*) FROM query_history").fetchone()[0]
        except sqlite3.Error:
            return 0