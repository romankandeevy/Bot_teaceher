import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import config
from scheduler import send_daily_post, deliver_post

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class SetTime(StatesGroup):
    waiting = State()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    chat_id = str(message.chat.id)

    if not config.CHAT_ID:
        from dotenv import set_key
        set_key(".env", "CHAT_ID", chat_id)
        config.CHAT_ID = chat_id

    await message.answer(
        "Привет! Я буду присылать тебе обучающие посты по стратегии и работе с топами.\n\n"
        f"📅 Ежедневно в {config.SEND_HOUR:02d}:{config.SEND_MINUTE:02d}\n\n"
        "Команды:\n"
        "/learn — получить пост прямо сейчас\n"
        "/settime — изменить время рассылки\n"
        "/time — узнать текущее время"
    )


@dp.message(Command("time"))
async def cmd_time(message: Message):
    await message.answer(f"Текущее время рассылки: {config.SEND_HOUR:02d}:{config.SEND_MINUTE:02d}")


@dp.message(Command("settime"))
async def cmd_settime(message: Message, state: FSMContext):
    await state.set_state(SetTime.waiting)
    await message.answer("Введи время в формате ЧЧ:ММ, например 08:30")


@dp.message(SetTime.waiting)
async def process_time(message: Message, state: FSMContext):
    text = message.text.strip()
    try:
        parts = text.split(":")
        hour = int(parts[0])
        minute = int(parts[1])
        assert 0 <= hour <= 23 and 0 <= minute <= 59
    except Exception:
        await message.answer("Неверный формат. Введи время как ЧЧ:ММ, например 09:00")
        return

    config.SEND_HOUR = hour
    config.SEND_MINUTE = minute

    try:
        from dotenv import set_key
        set_key(".env", "SEND_HOUR", str(hour))
        set_key(".env", "SEND_MINUTE", str(minute))
    except Exception:
        pass

    await state.clear()
    await message.answer(f"Время рассылки изменено на {hour:02d}:{minute:02d}")


@dp.message(Command("learn"))
async def cmd_learn(message: Message):
    await message.answer("Ищу статью и готовлю пост...")
    await deliver_post(bot, chat_id=str(message.chat.id))


async def main():
    asyncio.create_task(send_daily_post(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
