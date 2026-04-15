
from aiogram import types
from aiogram.filters.command import Command

from router import router
from loader import db
from enums import COMMANDS, how_to_collect_scores, how_to_lose_scores


@router.message(Command(commands=['docs'], prefix='/'))
async def docs(message: types.Message):
    # Send list of instructions to collect/lose score
    user_is_active = db.check_user_activation(telegram_id=message.from_user.id)

    if not user_is_active:
        await message.answer(text="Siz hali ro'yxatdan o'tishni yakunlamagansiz, avval ro'yxatdan o'tishni yakunlang")
        return

    text = "📈 Qanday qilib ball yig'ish mumkin ?\n\n"

    for key, values in how_to_collect_scores.items():
        text += f"<b>{key.title()}:</b>\n"
        for value in values:
            text += f"    ּ{value}.\n"

    text += "\n\n🔻 Qanday qilib ball yo'qotish mumkin ?\n\n"
    for value in how_to_lose_scores:
        text += f"    ּ{value}.\n"

    await message.answer(text=text, parse_mode="HTML")
