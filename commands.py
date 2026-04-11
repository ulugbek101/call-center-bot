from aiogram.types import BotCommand
from aiogram import Bot

from enums import COMMANDS


async def set_bot_commands(bot: Bot):
    # Set bot commands
    await bot.set_my_commands(
        commands=[
            BotCommand(command='/start', description='Botni ishga tushirish'),
            BotCommand(command='/help', description='Yordam olish'),
            BotCommand(command='/milestones', description='Yutuqlar ro\'yxatini ko\'rish'),
            # BotCommand(command='/leaderboard', description='Yutuqlar ro\'yxatini ko\'rish'),
        ],
        language_code="ru",
    )

    await bot.set_my_commands(
        commands=[
            BotCommand(command='/start', description='Botni ishga tushirish'),
            BotCommand(command='/help', description='Yordam olish'),
            BotCommand(command='/milestones', description='Yutuqlar ro\'yxatini ko\'rish'),
            # BotCommand(command='/leaderboard', description='Yutuqlar ro\'yxatini ko\'rish'),
        ],
        language_code="uz",
    )

    await bot.set_my_commands(
        commands=[
            BotCommand(command='/start', description='Botni ishga tushirish'),
            BotCommand(command='/help', description='Yordam olish'),
            BotCommand(command='/milestones', description='Yutuqlar ro\'yxatini ko\'rish'),
            # BotCommand(command='/leaderboard', description='Yutuqlar ro\'yxatini ko\'rish'),
        ],
        language_code="en",
    )
