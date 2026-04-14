from aiogram import types
from aiogram.filters import Command

from loader import db
from router import router


@router.message(Command(commands=["leaderboard"], prefix="/"))
async def send_milestones(message: types.Message):
    # Returns the leaderboard

    users = db.get_users()

    users_with_points = []
    for user in users:
        user_object = user.copy()
        user_points = db.get_user_points(user_id=user.get("id"))
        user_object.update({"points": user_points})
        users_with_points.append(user_object)

    leaders_rating = sorted(users_with_points, key=lambda x: x.get("points"))

    text = "📈 <b>Liderlar ro'yxati</b> 📈\n\n\n"

    for index, leader in enumerate(leaders_rating, start=1):
        text += f"{index}. {leader.get('first_name') or ''} {leader.get('last_name') or ''} - {leader.get('points')} ball\n\n"

    await message.answer(text=text, parse_mode="HTML")
