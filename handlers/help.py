
from aiogram import types
from aiogram.filters.command import Command

from router import router

from enums import COMMANDS


@router.message(Command(commands=['help'], prefix='/'))
async def help(message: types.Message):
    # Send help message to user representing commands list
    lines = ["📖 Mavjud buyruqlar:\n"]

    for cmd, desc in COMMANDS:
        lines.append(f"{cmd} — {desc}")

    text = "\n".join(lines)

    await message.answer(text)
