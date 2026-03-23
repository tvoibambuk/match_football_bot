from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database import add_match
import config
import datetime

router = Router()

@router.message(Command("add_match"))
async def admin_add_match(message: Message):
    if message.from_user.id not in config.ADMIN_IDS:
        return
    # Простой формат: /add_match Home Away 2024-12-31T20:00 1.9 3.2 2.1
    parts = message.text.split()
    if len(parts) != 7:
        await message.answer("Используй: /add_match Home Away YYYY-MM-DDTHH:MM odds_h odds_d odds_a")
        return
    _, home, away, time_str, odds_h, odds_d, odds_a = parts
    try:
        match_time = datetime.datetime.fromisoformat(time_str)
        add_match(home, away, match_time.isoformat(), float(odds_h), float(odds_d), float(odds_a))
        await message.answer("Матч добавлен")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")