from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import get_active_matches, place_bet, get_user_balance
from keyboards.inline import matches_menu, bet_options, back_to_main
import config

router = Router()

class BetState(StatesGroup):
    waiting_amount = State()

@router.callback_query(F.data == "matches")
async def show_matches(callback: CallbackQuery):
    matches = get_active_matches()
    if not matches:
        await callback.message.edit_text("Нет активных матчей", reply_markup=back_to_main())
        return
    text = "Выбери матч для ставки:"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=matches_menu(matches))
    await callback.answer()

@router.callback_query(F.data.startswith("match_"))
async def select_match(callback: CallbackQuery):
    match_id = int(callback.data.split("_")[1])
    # Здесь нужно получить матч из БД по match_id (упростим)
    # В реальности достаём из БД, для примера:
    # Временно достаём все матчи и ищем нужный
    matches = get_active_matches()
    match = next((m for m in matches if m["id"] == match_id), None)
    if not match:
        await callback.answer("Матч не найден")
        return
    text = (
        f"{match['home_team']} - {match['away_team']}\n"
        f"Коэффициенты:\n"
        f"П1: {match['odds_home']}  X: {match['odds_draw']}  П2: {match['odds_away']}"
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=bet_options(match_id, match['odds_home'], match['odds_draw'], match['odds_away'])
    )
    await callback.answer()

@router.callback_query(F.data.startswith("bet_"))
async def choose_bet(callback: CallbackQuery, state: FSMContext):
    _, match_id, bet_type, odds = callback.data.split("_")
    match_id = int(match_id)
    odds = float(odds)
    await state.update_data(match_id=match_id, bet_type=bet_type, odds=odds)
    text = "Введите сумму ставки (целое число):"
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(BetState.waiting_amount)
    await callback.answer()

@router.message(BetState.waiting_amount)
async def process_bet_amount(message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Введите положительное целое число")
        return
    
    user_id = message.from_user.id
    balance = get_user_balance(user_id)
    if amount > balance:
        await message.answer(f"Недостаточно средств. Ваш баланс: {balance}")
        return
    
    data = await state.get_data()
    match_id = data["match_id"]
    bet_type = data["bet_type"]
    odds = data["odds"]
    
    place_bet(user_id, match_id, bet_type, amount, odds)
    await message.answer(f"Ставка принята! Сумма: {amount}, коэффициент: {odds}, потенциальный выигрыш: {int(amount*odds)}")
    await state.clear()
    # Вернуть главное меню
    from keyboards.inline import main_menu
    await message.answer("Главное меню", reply_markup=main_menu())