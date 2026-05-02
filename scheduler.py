import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from aiogram import Bot
from db import get_all_users
from parser import fetch_random_article
from ai import summarize_article

MSK = ZoneInfo("Europe/Moscow")


async def send_daily_post(bot: Bot):
    while True:
        now = datetime.now(MSK)
        users = get_all_users()
        for user in users:
            if now.hour == user["send_hour"] and now.minute == user["send_minute"]:
                await deliver_post(bot, chat_id=user["chat_id"])
        await asyncio.sleep(30)


async def deliver_post(bot: Bot, chat_id: str):
    article = fetch_random_article()
    if not article:
        await bot.send_message(chat_id, "Не удалось найти новую статью. Попробуй позже.")
        return

    text = summarize_article(article["title"], article["summary"], article["url"])
    full_text = f"{text}\n\n🔗 {article['url']}"
    await bot.send_message(chat_id, full_text)
