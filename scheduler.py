import asyncio
from datetime import datetime
from aiogram import Bot
import config
from db import get_setting, init_db
from parser import fetch_random_article
from ai import summarize_article


def get_send_time():
    init_db()
    hour = get_setting("send_hour")
    minute = get_setting("send_minute")
    h = int(hour) if hour is not None else config.SEND_HOUR
    m = int(minute) if minute is not None else config.SEND_MINUTE
    return h, m


async def send_daily_post(bot: Bot):
    while True:
        now = datetime.now()
        h, m = get_send_time()
        if now.hour == h and now.minute == m:
            chat_id = get_setting("chat_id") or config.CHAT_ID
            if chat_id:
                await deliver_post(bot, chat_id=chat_id)
            await asyncio.sleep(61)
        else:
            await asyncio.sleep(30)


async def deliver_post(bot: Bot, chat_id: str = None):
    from db import get_setting
    target = chat_id or get_setting("chat_id") or config.CHAT_ID
    if not target:
        return

    article = fetch_random_article()
    if not article:
        await bot.send_message(target, "Не удалось найти новую статью. Попробуй позже.")
        return

    text = summarize_article(article["title"], article["summary"], article["url"])
    full_text = f"{text}\n\n🔗 {article['url']}"
    await bot.send_message(target, full_text)
