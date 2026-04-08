from aiogram.types import BotCommand
from aiogram import Bot


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/my_progress", description="Мой прогресс"),
        BotCommand(command="/my_achievements", description="Мои достижения"),
        BotCommand(command="/leaderboard", description="Доска лидеров"),
    ], language_code="ru")


    await bot.set_my_commands(commands=[
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/help", description="Yordam olish"),
        BotCommand(command="/my_progress", description="Mening progressim"),
        BotCommand(command="/my_achievements", description="Mening yutuqlarim"),
        BotCommand(command="/leaderboard", description="Liderlar doskasi"),
    ], language_code="uz")
