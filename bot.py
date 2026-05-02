import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import config
from db import init_db, get_setting, set_setting
from scheduler import send_daily_post, deliver_post

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class SetTime(StatesGroup):
    waiting = State()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    init_db()
    chat_id = str(message.chat.id)
    set_setting("chat_id", chat_id)

    h = int(get_setting("send_hour") or config.SEND_HOUR)
    m = int(get_setting("send_minute") or config.SEND_MINUTE)

    await message.answer(
        "Привет! Я буду присылать тебе обучающие посты по стратегии и работе с топами.\n\n"
        f"📅 Ежедневно в {h:02d}:{m:02d}\n\n"
        "Команды:\n"
        "/learn — получить пост прямо сейчас\n"
        "/settime — изменить время рассылки\n"
        "/time — узнать текущее время"
    )


@dp.message(Command("time"))
async def cmd_time(message: Message):
    h = int(get_setting("send_hour") or config.SEND_HOUR)
    m = int(get_setting("send_minute") or config.SEND_MINUTE)
    await message.answer(f"Текущее время рассылки: {h:02d}:{m:02d}")


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

    set_setting("send_hour", str(hour))
    set_setting("send_minute", str(minute))

    await state.clear()
    await message.answer(f"Время рассылки изменено на {hour:02d}:{minute:02d}")


@dp.message(Command("learn"))
async def cmd_learn(message: Message):
    await message.answer("Ищу статью и готовлю пост...")
    await deliver_post(bot, chat_id=str(message.chat.id))


async def main():
    init_db()
    asyncio.create_task(send_daily_post(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
