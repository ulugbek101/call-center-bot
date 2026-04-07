from aiogram.fsm.state import StatesGroup, State


class UserRegistration(StatesGroup):
    activation_code = State()
    first_name = State()
    last_name = State()
    middle_name = State()
    phone_number = State()
