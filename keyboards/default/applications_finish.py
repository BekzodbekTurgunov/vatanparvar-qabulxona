from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

finish_app = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Tasdiqlayman"),
            KeyboardButton("Bekor qilish")
        ],
        [
            KeyboardButton("Arizani qaytatdan yozish")
        ],
    ],
    resize_keyboard=True
)
