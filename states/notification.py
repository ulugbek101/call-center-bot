from aiogram.fsm.state import StatesGroup, State


class AdminNotification(StatesGroup):
    content = State()
