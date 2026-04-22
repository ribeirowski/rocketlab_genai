import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'banco.db'

def main():
    print(f"Using database: {DB_PATH}")
    if not DB_PATH.exists():
        print("Database file not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
    print("Tables:", tables)

    for t in tables:
        try:
            cnt = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        except Exception as e:
            cnt = f"error: {e}"
        print(f"- {t}: {cnt}")
        # show sample rows
        try:
            rows = cur.execute(f"SELECT * FROM {t} LIMIT 5").fetchall()
            for r in rows:
                print("   ", dict(r))
        except Exception as e:
            print("   sample error:", e)

    conn.close()

if __name__ == '__main__':
    main()
