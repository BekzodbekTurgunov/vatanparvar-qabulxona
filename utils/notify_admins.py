import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher, message_text):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, message_text)

        except Exception as err:
            logging.exception(err)
