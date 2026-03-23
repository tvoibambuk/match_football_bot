import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from config import BOT_TOKEN, RAILWAY_ENVIRONMENT, PORT
from database import init_db
from handlers import start, profile, matches, admin
from utils.helpers import scheduled_match_fetch

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def on_startup(bot: Bot):
    """Действия при запуске бота"""
    logger.info("Бот запускается...")
    
    # Инициализация базы данных
    init_db()
    logger.info("База данных инициализирована")
    
    # Запуск фоновых задач
    asyncio.create_task(scheduled_match_fetch(bot))
    logger.info("Фоновые задачи запущены")
    
    # Установка вебхука если в Railway окружении
    if RAILWAY_ENVIRONMENT:
        webhook_url = f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN', 'localhost')}/webhook"
        await bot.set_webhook(webhook_url)
        logger.info(f"Вебхук установлен: {webhook_url}")

async def on_shutdown(bot: Bot):
    """Действия при остановке бота"""
    logger.info("Бот останавливается...")
    
    # Удаляем вебхук при остановке
    if RAILWAY_ENVIRONMENT:
        await bot.delete_webhook()
        logger.info("Вебхук удален")

async def main():
    """Основная функция запуска бота"""
    bot = Bot(token=8341059407:AAHNEtZ1g2iLhlgGU6MzvxT--50yJ28gF8U)
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(matches.router)
    dp.include_router(admin.router)
    
    if RAILWAY_ENVIRONMENT:
        # Режим вебхука для Railway
        app = web.Application()
        
        # Настройка healthcheck для Railway
        async def health_handler(request):
            return web.Response(text="OK", status=200)
        
        app.router.add_get("/health", health_handler)
        
        # Настройка вебхука
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        webhook_requests_handler.register(app, path="/webhook")
        setup_application(app, dp, bot=bot)
        
        # Запуск веб-сервера
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        
        logger.info(f"Бот запущен в режиме вебхука на порту {PORT}")
        
        # Держим приложение запущенным
        await asyncio.Event().wait()
    else:
        # Режим polling для локальной разработки
        logger.info("Бот запущен в режиме polling")
        
        # Запускаем фоновые задачи
        asyncio.create_task(scheduled_match_fetch(bot))
        
        # Запускаем polling
        await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        sys.exit(1)