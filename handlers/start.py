from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters.command import CommandStart

from router import router
from states.registration import UserRegistration


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    # Greet the user and request activation_code
    await message.answer(text=f"Assalomu alaykum, {message.from_user.full_name} 👋")
    await message.answer(text="Davom etish uchun, iltimos, aktivatsion kodni kiriting 👇")
    await state.set_state(UserRegistration.activation_code)
