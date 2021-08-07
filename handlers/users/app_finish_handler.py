from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from handlers.users.applications_handler import form_application, save_data


@dp.message_handler(text='Tasdiqlayman')
async def confirm(message: types.Message):
    await save_data(message)


@dp.message_handler(text='Bekor qilish')
async def confirm(message: types.Message):
    await message.answer("Arizangiz bekor qilindi!")
    # await state.finish()


@dp.message_handler(text='Arizani qaytatdan yozish')
async def confirm(message: types.Message):
    await form_application(message)
    # await state.finish()