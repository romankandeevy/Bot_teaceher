import feedparser
import random
import sqlite3
from config import RSS_FEEDS

DB_PATH = "used_articles.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS used (url TEXT PRIMARY KEY)")
    conn.commit()
    conn.close()


def is_used(url: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT 1 FROM used WHERE url=?", (url,))
    result = cur.fetchone()
    conn.close()
    return result is not None


def mark_used(url: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR IGNORE INTO used VALUES (?)", (url,))
    conn.commit()
    conn.close()


def fetch_random_article() -> dict | None:
    init_db()
    feeds = RSS_FEEDS.copy()
    random.shuffle(feeds)

    candidates = []
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                url = entry.get("link", "")
                if url and not is_used(url):
                    title = entry.get("title", "")
                    summary = entry.get("summary", entry.get("description", ""))
                    if title and summary:
                        candidates.append({
                            "url": url,
                            "title": title,
                            "summary": summary,
                        })
        except Exception:
            continue

    if not candidates:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM used")
        conn.commit()
        conn.close()
        return fetch_random_article()

    article = random.choice(candidates)
    mark_used(article["url"])
    return article
