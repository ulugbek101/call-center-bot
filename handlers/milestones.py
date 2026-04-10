from aiogram import types
from aiogram.filters import Command

from loader import db
from router import router


@router.message(Command(commands=["milestones"], prefix="/"))
async def send_milestones(message: types.Message):
    # Return available achiements list
    milestones = db.get_milestones()
    user_score, user_milestone = db.get_user_progress(telegram_id=message.from_user.id)

    text = "🏁 <b>Yutuqlar ro'yxati</b> 🏁\n\n" if len(milestones) > 0 else "Ro'yxat hozircha bo'sh"

    text += f"<i>Sizda mavjud ball: {user_score or 0}</i>\n\n\n"

    for index, milestone in enumerate(milestones, start=1):
        row_text = f"<b>{milestone.get('required_score')} ball</b> - <b>{milestone.get('name')}</b>"

        if (user_score or 0) >= milestone.get("required_score"):
            text += f"<s>{row_text}</s> ✅" + "\n\n"
        else:
            text += row_text + "\n\n"

    await message.answer(text=text, parse_mode="HTML")
