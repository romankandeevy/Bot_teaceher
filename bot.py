import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import config
from scheduler import send_daily_post, deliver_post

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    chat_id = str(message.chat.id)

    if not config.CHAT_ID:
        import os
        from dotenv import set_key
        set_key(".env", "CHAT_ID", chat_id)
        config.CHAT_ID = chat_id

    await message.answer(
        "Привет! Я буду присылать тебе обучающие посты по стратегии и работе с топами.\n\n"
        f"📅 Ежедневно в {config.SEND_HOUR:02d}:{config.SEND_MINUTE:02d}\n"
        "📚 Команды:\n"
        "/learn — получить пост прямо сейчас\n"
        "/start — приветствие и настройка"
    )


@dp.message(Command("learn"))
async def cmd_learn(message: Message):
    await message.answer("Ищу статью и готовлю пост...")
    await deliver_post(bot, chat_id=str(message.chat.id))


async def main():
    asyncio.create_task(send_daily_post(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
