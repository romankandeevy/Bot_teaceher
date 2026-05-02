import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")
SEND_HOUR = int(os.getenv("SEND_HOUR", 9))
SEND_MINUTE = int(os.getenv("SEND_MINUTE", 0))

RSS_FEEDS = [
    "https://hbr.org/resources/rss/recent",
    "https://feeds.feedburner.com/mitsloan/news",
    "https://www.mckinsey.com/insights/rss",
    "https://www.strategy-business.com/rss",
    "https://feeds.feedburner.com/fastcompany/headlines",
]
