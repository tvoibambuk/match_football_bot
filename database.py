import sqlite3
import datetime
from config import DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
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

def get_user_balance(user_id):
    with get_db_connection() as conn:
        row = conn.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return row["balance"] if row else 0

def update_balance(user_id, amount):
    with get_db_connection() as conn:
        conn.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

def register_user(user_id):
    with get_db_connection() as conn:
        conn.execute("INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)", (user_id, 0))
        conn.commit()

def can_claim_daily_bonus(user_id):
    with get_db_connection() as conn:
        row = conn.execute("SELECT last_bonus FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not row or row["last_bonus"] is None:
            return True
        last = datetime.datetime.fromisoformat(row["last_bonus"])
        now = datetime.datetime.now()
        return (now - last).total_seconds() >= 86400

def claim_daily_bonus(user_id):
    with get_db_connection() as conn:
        now = datetime.datetime.now().isoformat()
        conn.execute("UPDATE users SET balance = balance + ?, last_bonus = ? WHERE user_id = ?",
                     (config.DAILY_BONUS, now, user_id))
        conn.commit()

def add_match(home, away, match_time, odds_h, odds_d, odds_a):
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO matches (home_team, away_team, match_time, odds_home, odds_draw, odds_away) VALUES (?,?,?,?,?,?)",
            (home, away, match_time, odds_h, odds_d, odds_a)
        )
        conn.commit()

def get_active_matches():
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM matches WHERE status = 'active' ORDER BY match_time").fetchall()

def place_bet(user_id, match_id, bet_type, amount, odds):
    with get_db_connection() as conn:
        potential = int(amount * odds)
        conn.execute(
            "INSERT INTO bets (user_id, match_id, bet_type, amount, odds, potential_win) VALUES (?,?,?,?,?,?)",
            (user_id, match_id, bet_type, amount, odds, potential)
        )
        conn.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

def get_user_bets(user_id):
    with get_db_connection() as conn:
        return conn.execute('''
            SELECT b.*, m.home_team, m.away_team, m.match_time
            FROM bets b
            JOIN matches m ON b.match_id = m.id
            WHERE b.user_id = ?
            ORDER BY b.created_at DESC
        ''', (user_id,)).fetchall()