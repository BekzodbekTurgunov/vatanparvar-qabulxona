from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

finish_app = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Tasdiqlayman"),
            KeyboardButton("Bekor qilish")
        ],
        [
            KeyboardButton("Qayta yuborish")
        ],
    ],
    resize_keyboard=True
)
