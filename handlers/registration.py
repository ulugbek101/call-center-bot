import re

from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from router import router
from states.registration import UserRegistration
from loader import db


@router.message(UserRegistration.activation_code)
async def save_activation_code(message: types.Message, state: FSMContext):
    # Save activation code and request first_name
    activation_code = message.text

    await state.update_data(activation_code=activation_code)

    # Get the user from database
    user = db.get_user(activation_code=activation_code)

    # User activation
    db.activate_user(activation_code=activation_code, telegram_id=message.from_user.id)

    # Proceed registration
    if user:
        await message.answer(text="Aktivatsiya kodi qabul qilindi ✅", protect_content=True)
        await message.answer(text="Ismingizni kiriting 👇", protect_content=True)
        await state.set_state(UserRegistration.first_name)
    else:
        await message.answer(text="Aktivatsiya kodi noto'g'ri, iltimos, qayta tering yoki mas'ul insonga aloqaga chiqing", protect_content=True)


@router.message(UserRegistration.first_name)
async def save_first_name(message: types.Message, state: FSMContext):
    # Save first_name and request last_name
    first_name = message.text

    # Save user's first_name to database
    db.save_attribute(attribute_name="first_name", value=first_name, telegram_id=message.from_user.id)
    await message.answer(text="Ismingiz muvaffaqiyatli saqlandi ✅", protect_content=True)

    # Request last_name
    await message.answer(text="Familiyangizni kiriting 👇", protect_content=True)
    await state.set_state(UserRegistration.last_name)


@router.message(UserRegistration.last_name)
async def save_last_name(message: types.Message, state: FSMContext):
    # Save last_name and request middle_name
    last_name = message.text

    # Save user's last_name to database
    db.save_attribute(attribute_name="last_name", value=last_name, telegram_id=message.from_user.id)
    await message.answer(text="Familiyangiz muvaffaqiyatli saqlandi ✅", protect_content=True)

    # Request last_name
    await message.answer(text="Sharifingizni kiriting 👇", protect_content=True)
    await state.set_state(UserRegistration.middle_name)


@router.message(UserRegistration.middle_name)
async def save_middle_name(message: types.Message, state: FSMContext):
    # Save middle_name and request phone_number
    middle_name = message.text

    # Save user's middle_name to database
    db.save_attribute(attribute_name="middle_name", value=middle_name, telegram_id=message.from_user.id)
    await message.answer(text="Sharifingiz muvaffaqiyatli saqlandi ✅", protect_content=True)

    # Request phone_number
    await message.answer(text="Telefon raqamingizni kiriting 👇 yoki tugmani bosish orqali yuboring", protect_content=True)
    await message.answer(
        text="Telefon raqamni tugma orqali yuboring yoki quyidagicha formatda kiriting:\n1. +998996937308\n2. +998 99 693 73 08",
        reply_markup=ReplyKeyboardBuilder().button(text="📞 Telefon raqamimni ulashish", request_contact=True).as_markup(resize_keyboard=True)
    , protect_content=True)
    await state.set_state(UserRegistration.phone_number)


@router.message(UserRegistration.phone_number)
async def save_phone_number(message: types.Message, state: FSMContext):
    # Save phone_number and finish registration
    if message.contact:
        phone_number = message.contact.phone_number
    elif message.text:
        phone_number = message.text.replace(' ', '').strip()
    else:
        await message.answer(
            text="Telefon raqamni matn ko'rinishida yoki tugma orqali yuboring", protect_content=True
        )
        return

    # Add "+" sign to the beginning of a phone number
    if not phone_number.startswith("+"):
        phone_number = f"+{phone_number}"

    # Phone number pattern to check phone number format to be +998996937308 only
    pattern = r'^\+998\d{9}$'

    if re.match(pattern=pattern, string=phone_number):
        try:
            db.save_attribute(attribute_name="phone_number", value=phone_number, telegram_id=message.from_user.id)
        except Exception as exp:
            await message.answer(text="Telefon raqam avval ro'yatga olingan", protect_content=True)
            return
        await message.answer(
            text="Telefon raqamingiz muvaffaqiyatli saqlandi ✅",
            reply_markup=types.ReplyKeyboardRemove(), protect_content=True
        )
        await message.answer(text="Siz muvaffaqiyatli ro'yxatga olindingiz, raxmat!", protect_content=True)
        await state.clear()
    else:
        await message.answer(
            text="Telefon raqam noto'g'ri formatda kiritildi, tekshirib qaytadan kiriting.\n"
                 "Masalan:\n"
                 "1. +998996937308\n"
                 "2. +998 99 693 73 08",
            protect_content=True
        )
