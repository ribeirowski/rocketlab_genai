import sqlite3
from app.config import get_settings

class BaseRepository:
    def __init__(self):
        self.db_path = get_settings().DATABASE_PATH

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn