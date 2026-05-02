import sqlite3

DB_PATH = "used_articles.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS used (url TEXT PRIMARY KEY)")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id TEXT PRIMARY KEY,
            send_hour INTEGER DEFAULT 9,
            send_minute INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def add_user(chat_id: str, hour: int = 9, minute: int = 0):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO users (chat_id, send_hour, send_minute) VALUES (?,?,?)",
        (chat_id, hour, minute)
    )
    conn.commit()
    conn.close()


def set_user_time(chat_id: str, hour: int, minute: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE users SET send_hour=?, send_minute=? WHERE chat_id=?",
        (hour, minute, chat_id)
    )
    conn.commit()
    conn.close()


def get_user_time(chat_id: str) -> tuple[int, int]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT send_hour, send_minute FROM users WHERE chat_id=?", (chat_id,))
    row = cur.fetchone()
    conn.close()
    return (row[0], row[1]) if row else (9, 0)


def get_all_users() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT chat_id, send_hour, send_minute FROM users")
    rows = cur.fetchall()
    conn.close()
    return [{"chat_id": r[0], "send_hour": r[1], "send_minute": r[2]} for r in rows]
