import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла (локально)
load_dotenv()

# Конфигурация бота
BOT_TOKEN = os.getenv("8341059407:AAHNEtZ1g2iLhlgGU6MzvxT--50yJ28gF8U)
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

# ID администраторов (можно передать как строку через запятую)
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()] if ADMIN_IDS_STR else []

# Настройки базы данных
DB_PATH = os.getenv("DB_PATH", "database.db")

# Настройки бота
DAILY_BONUS = int(os.getenv("DAILY_BONUS", "1000"))
MATCH_UPDATE_INTERVAL = int(os.getenv("MATCH_UPDATE_INTERVAL", "21600"))  # 6 часов в секундах

# Настройки для Railway
RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT", False)
PORT = int(os.getenv("PORT", 8080))

# Настройки парсинга (если используешь API)
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")
USE_REAL_API = bool(os.getenv("USE_REAL_API", False))