import asyncio
from datetime import datetime
from aiogram import Bot
from config import CHAT_ID, SEND_HOUR, SEND_MINUTE
from parser import fetch_random_article
from ai import summarize_article


async def send_daily_post(bot: Bot):
    while True:
        now = datetime.now()
        if now.hour == SEND_HOUR and now.minute == SEND_MINUTE:
            await deliver_post(bot)
            await asyncio.sleep(61)
        else:
            await asyncio.sleep(30)


async def deliver_post(bot: Bot, chat_id: str = None):
    target = chat_id or CHAT_ID
    if not target:
        return

    article = fetch_random_article()
    if not article:
        await bot.send_message(target, "Не удалось найти новую статью. Попробуй позже.")
        return

    text = summarize_article(article["title"], article["summary"], article["url"])
    full_text = f"{text}\n\n🔗 {article['url']}"

    await bot.send_message(target, full_text)
