import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers import start, profile, matches, admin
from utils.fetcher import fetch_upcoming_matches
from utils.helpers import scheduled_match_fetch

async def main():
    logging.basicConfig(level=logging.INFO)
    init_db()
    
    bot = Bot(token=8341059407:AAHNEtZ1g2iLhlgGU6MzvxT--50yJ28gF8U)
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(matches.router)
    dp.include_router(admin.router)
    
    # Запускаем периодическое обновление матчей (каждые 6 часов)
    asyncio.create_task(scheduled_match_fetch(bot))
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())