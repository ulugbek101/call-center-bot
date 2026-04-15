from aiogram import types
from aiogram.filters.command import Command

from router import router
from loader import db
from enums import COMMANDS


@router.message(Command(commands=['help'], prefix='/'))
async def docs(message: types.Message):
    # Send list of available commands
    user_is_active = db.check_user_activation(telegram_id=message.from_user.id)

    if not user_is_active:
        await message.answer(text="Siz hali ro'yxatdan o'tishni yakunlamagansiz, avval ro'yxatdan o'tishni yakunlang", protect_content=True)
        return

    text = "📖 Mavjud buyruqlar:\n\n"

    for command in COMMANDS:
        text += f"{command[0]} - {command[-1]}\n"

    await message.answer(text, protect_content=True)
