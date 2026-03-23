from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.inline import main_menu
from database import register_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    register_user(user_id)
    text = (
        "Добро пожаловать в футбольный тотализатор\n\n"
        "<b>Зарабатывай каждый день</b>\n"
        "<i>Делай ставки на топ-матчи</i>\n"
        "Используй меню ниже для навигации"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu())

@router.callback_query(F.data == "main")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_menu(callback: CallbackQuery):
    text = (
        "Помощь по боту\n\n"
        "• Пополнить баланс можно через ежедневный бонус\n"
        "• Выбери матч → выбери исход → укажи сумму\n"
        "• Ставка забирает деньги с баланса\n"
        "• После окончания матча выигрыш начисляется автоматически\n"
        "• По всем вопросам пиши админу"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main())
    await callback.answer()