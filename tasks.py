import logging
from random import choice

from loader import bot, db
from config import ADMINS


async def send_random_motivational_phrase():
    """
    Send random motivational phrase from database to users
    :return: None
    """
    successes = []
    fails = []

    # Return staffs list from database
    staffs = db.get_staffs()

    # Motivational phrases from database
    motivational_phrases = db.get_motivational_phrases()

    # Sending random motivational phrase to staffs only if there is at least 1 staff and at least 1 motivational phrase
    if len(staffs) > 0 and len(motivational_phrases) > 0:
        for staff in staffs:
            try:
                await bot.send_message(
                    chat_id=staff.get("telegram_id"),
                    text=choice(seq=motivational_phrases).get("phrase"),
                )
                successes.append(staff)
            except Exception as exp:
                fails.append(staff)
                logging.warning(f"Error while sending motivational phrase to staff. Error: {exp.__class__.__name__} - {exp}")

    # Send report to admins - to what amount of staffs phrase was sent
    text = f"Ruhlantiruvchi jumla jamoaga {'yuborildi' if len(motivational_phrases) > 0 and len(staffs) > 0 else 'yuborilmadi'}\n\n"

    text += f"Xodimlar soni: {len(staffs)}\n"
    text += f"Muvaffaqiyatli yuborishlar soni: {len(successes)}\n"
    text += f"Yuborib bo'lmaganlar soni: {len(fails)}\n\n"

    if len(fails) > 0:
        failed_staffs = ", ".join([f"{fail.get('first_name')} {fail.get('last_name')}".title() for fail in fails])
        text += f"Yuborib bo'lmaganlar xodimlar: {failed_staffs}"

    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=text,
            )
        except Exception as exp:
            logging.warning(f"Error while sending report about success/failed motivational messages. Error: {exp.__class__.__name__} - {exp}")
