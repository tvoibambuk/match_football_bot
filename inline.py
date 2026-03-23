from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Матчи", callback_data="matches")],
        [InlineKeyboardButton(text="Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Ежедневный бонус", callback_data="bonus")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")]
    ])

def matches_menu(matches):
    buttons = []
    for match in matches:
        text = f"{match['home_team']} - {match['away_team']}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"match_{match['id']}")])
    buttons.append([InlineKeyboardButton(text="Главное меню", callback_data="main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def bet_options(match_id, odds_h, odds_d, odds_a):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"П1 {odds_h}", callback_data=f"bet_{match_id}_home_{odds_h}")],
        [InlineKeyboardButton(text=f"X {odds_d}", callback_data=f"bet_{match_id}_draw_{odds_d}")],
        [InlineKeyboardButton(text=f"П2 {odds_a}", callback_data=f"bet_{match_id}_away_{odds_a}")],
        [InlineKeyboardButton(text="Назад", callback_data="matches")]
    ])

def back_to_main():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Главное меню", callback_data="main")]
    ])