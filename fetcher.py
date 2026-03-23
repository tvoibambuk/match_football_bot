import random
import datetime

def fetch_upcoming_matches():
    """
    В реальности здесь был бы запрос к API, парсинг сайта.
    Возвращаем список словарей для теста.
    """
    matches = []
    now = datetime.datetime.now()
    for i in range(1, 4):
        match_time = now + datetime.timedelta(hours=i*24)
        matches.append({
            "home": f"TeamHome{i}",
            "away": f"TeamAway{i}",
            "time": match_time.isoformat(),
            "odds_h": round(random.uniform(1.5, 3.0), 2),
            "odds_d": round(random.uniform(3.0, 4.5), 2),
            "odds_a": round(random.uniform(1.5, 3.0), 2)
        })
    return matches