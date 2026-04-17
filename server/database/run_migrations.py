import sqlite3
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from app.config import get_settings

def run():
    db_path = Path(__file__).parent.parent / get_settings().DATABASE_PATH
    migrations_dir = Path(__file__).parent / "migrations" 

    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename TEXT PRIMARY KEY,
                applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        applied = {row[0] for row in conn.execute("SELECT filename FROM schema_migrations")}

        applied_count = 0
        skipped_count = 0

        for sql_file in sorted(migrations_dir.glob("*.sql")):
            if sql_file.name in applied:
                print(f"  ⏭  Skipping {sql_file.name} (already applied)")
                skipped_count += 1
                continue
            print(f"  ✔  Applying {sql_file.name}...")
            conn.executescript(sql_file.read_text())
            conn.execute("INSERT INTO schema_migrations (filename) VALUES (?)", (sql_file.name,))
            applied_count += 1

        print(f"\nDone. {applied_count} applied, {skipped_count} skipped.")
        
if __name__ == "__main__":
    run()