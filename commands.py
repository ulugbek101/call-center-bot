from aiogram.types import BotCommand
from aiogram import Bot

from enums import COMMANDS


async def set_bot_commands(bot: Bot):
    # Set bot commands
    await bot.set_my_commands(
        commands=list(map(lambda cmd: BotCommand(command=cmd[0], description=cmd[1]), COMMANDS))
    )
