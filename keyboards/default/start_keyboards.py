from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Ariza yuborish'),
            KeyboardButton('yordam')
        ],
    ],
    resize_keyboard=True
)
