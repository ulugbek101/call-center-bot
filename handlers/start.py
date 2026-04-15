from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters.command import CommandStart

from router import router
from states.registration import UserRegistration
from loader import db


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    # Greet the user and request activation_code
    is_active_user = db.check_user_activation(telegram_id=message.from_user.id)

    if not is_active_user:
        await message.answer(text=f"Assalomu alaykum, {message.from_user.full_name} 👋", protect_content=True)
        await message.answer(text="Davom etish uchun, iltimos, aktivatsion kodni kiriting 👇", protect_content=True)
        await state.set_state(UserRegistration.activation_code)
