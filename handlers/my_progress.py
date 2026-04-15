from aiogram import types
from aiogram.filters.command import Command

from loader import db
from router import router


@router.message(Command(commands=['my_progress'], prefix='/'))
async def my_progress(message: types.Message):
    # Show user's progress

    # Finish function here if user has not completed the registration yet
    user_is_active = db.check_user_activation(telegram_id=message.from_user.id)
    if not user_is_active:
        return

    current_score, current_milestone = db.get_user_progress(telegram_id=message.from_user.id)

    text = "🏳️ <b>Sizning progressingiz</b> 🏳️\n\n"
    text += f"Yig'ilgan ball: <b>{current_score} ball</b>\n"
    text += f"Oxrigi yutuq: <b>{current_milestone if current_milestone else 'Mavjud emas'}</b>"

    await message.answer(text=text, parse_mode="HTML", protect_content=True)
