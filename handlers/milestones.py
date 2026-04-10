from aiogram import types
from aiogram.filters import Command

from loader import db
from router import router


@router.message(Command(commands=["milestones"], prefix="/"))
async def send_milestones(message: types.Message):
    # Return available achiements list
    milestones = db.get_milestones()

    text = "--- Yutuqlar ro'yxati ---\n\n" if len(milestones) > 0 else "Ro'yxat hozircha bo'sh"

    for index, milestone in enumerate(milestones, start=1):
        text += f"Kerakli ball: <b>{milestone.get('required_score')} ball</b>\n"
        text += f"Yutuq:          <b>{milestone.get('name')}</b>\n\n"

    await message.answer(text=text, parse_mode="HTML")
