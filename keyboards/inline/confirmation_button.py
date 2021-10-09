from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callback_data.confirmation_data import confirmation_callback

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Tasdiqlash', callback_data=confirmation_callback.new(action='confirm')),
            InlineKeyboardButton(text='❌ Bekor qilish', callback_data=confirmation_callback.new(action='cancel')),
        ]
    ]
)