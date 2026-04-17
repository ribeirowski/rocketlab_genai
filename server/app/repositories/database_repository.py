import sqlite3
import logging

from app.config import get_settings
from app.exceptions import DatabaseQueryException
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class DatabaseRepository(BaseRepository):
    SQL_WRITE_KEYWORDS = frozenset(
        {"DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "CREATE"}
    )

    def __init__(self):
        super().__init__()

    def get_schema(self) -> str:
        try:
            with self._connect() as conn:
                tables = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                ).fetchall()
                parts = []
                for table in tables:
                    cols = conn.execute(f"PRAGMA table_info({table['name']})").fetchall()
                    col_def = ", ".join(f"{c['name']} {c['type']}" for c in cols)
                    parts.append(f"-- {table['name']}\nCREATE TABLE {table['name']} ({col_def});")
                return "\n\n".join(parts)
        except sqlite3.Error as e:
            raise DatabaseQueryException(f"Failed to read schema: {e}") from e

    def get_tables(self) -> list[str]:
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                ).fetchall()
                return [row["name"] for row in rows]
        except sqlite3.Error as e:
            raise DatabaseQueryException(f"Failed to list tables: {e}") from e

    def is_safe_sql(self, sql: str) -> bool:
        return not any(kw in sql.upper() for kw in self.SQL_WRITE_KEYWORDS)

    def execute_read_query(self, sql: str) -> list[dict]:
        limit = get_settings().QUERY_RESULT_LIMIT
        limited_sql = f"SELECT * FROM ({sql.rstrip(';')}) LIMIT {limit}"
        try:
            with self._connect() as conn:
                rows = conn.execute(limited_sql).fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error("Query error | SQL: %s | Error: %s", sql, e)
            raise DatabaseQueryException(f"Execution error: {e}") from e

    def health_check(self) -> bool:
        try:
            with self._connect() as conn:
                conn.execute("SELECT 1")
            return True
        except sqlite3.Error:
            return False