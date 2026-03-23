from aiogram import Router, F
from aiogram.types import CallbackQuery
from database import get_user_balance, can_claim_daily_bonus, claim_daily_bonus, get_user_bets
from keyboards.inline import back_to_main
import config

router = Router()

@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    balance = get_user_balance(user_id)
    bets = get_user_bets(user_id)
    total_bets = len(bets)
    # Простая статистика
    won = sum(1 for b in bets if b["status"] == "won")
    lost = sum(1 for b in bets if b["status"] == "lost")
    
    text = (
        f"Профиль игрока\n\n"
        f"Баланс: {balance}\n"
        f"Всего ставок: {total_bets}\n"
        f"Выиграно: {won}\n"
        f"Проиграно: {lost}\n"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main())
    await callback.answer()

@router.callback_query(F.data == "bonus")
async def daily_bonus(callback: CallbackQuery):
    user_id = callback.from_user.id
    if can_claim_daily_bonus(user_id):
        claim_daily_bonus(user_id)
        text = f"Бонус получен! +{config.DAILY_BONUS}"
    else:
        text = "Вы уже получали бонус сегодня. Попробуйте завтра."
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main())
    await callback.answer()