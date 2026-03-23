import os
import sqlite3
import datetime
import logging
from config import DB_PATH, RAILWAY_ENVIRONMENT

logger = logging.getLogger(__name__)

# Если на Railway и есть переменная DATABASE_URL, используем PostgreSQL
if RAILWAY_ENVIRONMENT and os.getenv("DATABASE_URL"):
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        USE_POSTGRES = True
        logger.info("Используем PostgreSQL для базы данных")
    except ImportError:
        USE_POSTGRES = False
        logger.warning("psycopg2 не установлен, используем SQLite")
else:
    USE_POSTGRES = False

def get_db_connection():
    if USE_POSTGRES:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Инициализация базы данных"""
    with get_db_connection() as conn:
        if USE_POSTGRES:
            # PostgreSQL schema
            with conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        balance INTEGER DEFAULT 0,
                        last_bonus TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS matches (
                        id SERIAL PRIMARY KEY,
                        home_team TEXT,
                        away_team TEXT,
                        match_time TIMESTAMP,
                        odds_home REAL,
                        odds_draw REAL,
                        odds_away REAL,
                        status TEXT DEFAULT 'active'
                    )
                ''')
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS bets (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT,
                        match_id INTEGER,
                        bet_type TEXT,
                        amount INTEGER,
                        odds REAL,
                        potential_win INTEGER,
                        status TEXT DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        else:
            # SQLite schema
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    balance INTEGER DEFAULT 0,
                    last_bonus TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    home_team TEXT,
                    away_team TEXT,
                    match_time TIMESTAMP,
                    odds_home REAL,
                    odds_draw REAL,
                    odds_away REAL,
                    status TEXT DEFAULT 'active'
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS bets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    match_id INTEGER,
                    bet_type TEXT,
                    amount INTEGER,
                    odds REAL,
                    potential_win INTEGER,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id),
                    FOREIGN KEY(match_id) REFERENCES matches(id)
                )
            ''')
            conn.commit()
    
    logger.info("База данных инициализирована")

# Остальные функции нужно адаптировать для работы с обоими типами БД
# Вот пример адаптации для get_user_balance:

def get_user_balance(user_id):
    with get_db_connection() as conn:
        if USE_POSTGRES:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
                row = cur.fetchone()
                return row["balance"] if row else 0
        else:
            row = conn.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return row["balance"] if row else 0