from aiogram.types import BotCommand
from aiogram import Bot

from enums import COMMANDS


async def set_bot_commands(bot: Bot):
    # Set bot commands
    commands = []

    for command in COMMANDS:
        commands.append(
            BotCommand(command=command[0], description=command[1])
        )

    await bot.set_my_commands(
        commands=commands
    )
