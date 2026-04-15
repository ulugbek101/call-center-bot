from aiogram import types, F
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from states.notification import AdminNotification
from router import router
from loader import db
from config import ADMINS


@router.message(Command(commands=['elon'], prefix='/'))
async def send_notification(message: types.Message, state: FSMContext):
    # Start sending notification to all users
    user_is_admin = str(message.from_user.id) in ADMINS

    if not user_is_admin:
        return

    markup = ReplyKeyboardBuilder()
    markup.button(text="Bekor qilish")

    await message.answer("E'lon matnini yozing 👇", reply_markup=markup.as_markup(resize_keyboard=True), protect_content=True)
    await state.set_state(AdminNotification.content)


@router.message(AdminNotification.content, F.text == "Bekor qilish")
async def cancel_notification(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("E'lon yuborish bekor qilindi ✅", reply_markup=types.ReplyKeyboardRemove(), protect_content=True)


@router.message(AdminNotification.content)
async def forward_notification_to_all_users(message: types.Message, state: FSMContext):
    users = db.get_users()

    success_count = 0
    fail_count = 0
    failed = []

    for user in users:
        try:
            await message.copy_to(chat_id=user.get('telegram_id'), protect_content=True)
            success_count += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            fail_count += 1
            failed.append(f"{user.get('first_name', '').title()} {user.get('last_name', '').title()}")
        except Exception:
            fail_count += 1
            failed.append(f"{user.get('first_name', '')} {user.get('last_name', '')}")

    await state.clear()

    text = f"E'lon yuborildi ✅\n\n"
    text += f"Yuborilgan xodimlar soni: {success_count} ta\n"
    text += f"Yuborilmagan xodimlar soni: {fail_count} ta\n"

    if fail_count > 0:
        text += f"\nKimlarga yuborib bo'lmadi: {', '.join(failed)}"

    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardRemove(),
        protect_content=True
    )
