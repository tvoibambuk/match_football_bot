import asyncio
from utils.fetcher import fetch_upcoming_matches
from database import add_match

async def scheduled_match_fetch(bot):
    while True:
        # Обновляем матчи каждые 6 часов
        await asyncio.sleep(21600)
        matches = fetch_upcoming_matches()
        for m in matches:
            add_match(m["home"], m["away"], m["time"], m["odds_h"], m["odds_d"], m["odds_a"])
        # Оповещаем админов
        # await bot.send_message(admin_id, "Матчи обновлены")