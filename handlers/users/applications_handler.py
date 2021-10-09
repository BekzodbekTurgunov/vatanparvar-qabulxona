from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.applications import Applications
from keyboards.default.applications_finish import finish_app
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from utils.notify_admins import on_startup_notify
from keyboards.default.start_keyboards import start_menu
from keyboards.inline.confirmation_button import confirmation_keyboard
from keyboards.callback_data.confirmation_data import confirmation_callback
from data.config import IP, ADMINS
import requests
from pprint import pprint as print

data_local = []


@dp.message_handler(commands='ariza')
@dp.message_handler(text='Ariza yuborish')
async def form_application(message: Message):
    await message.reply("Iltimos ismingizni kiriting: ", reply_markup=ReplyKeyboardRemove())
    await Applications.first_name.set()


@dp.message_handler(state=Applications.first_name)
async def get_first_name(message: Message, state: FSMContext):
    first_name = message.text
    if len(first_name) < 3:
        await message.reply("Iltimos ismingizni to'gri kiriting:")
        await Applications.first_name.set()
        return
    await state.update_data(first_name=first_name)
    await message.answer("Familyangizni kiriting:")
    await Applications.next()


@dp.message_handler(state=Applications.last_name)
async def get_last_name(message: Message, state: FSMContext):
    last_name = message.text
    if len(last_name) < 3:
        await message.reply("Iltimos familyangizni togri kiriting:")
        await Applications.last_name.set()
        return
    await state.update_data(last_name=last_name)
    await message.answer("Murojot uchun telefoningizni kiriting: (998901234567 ko'rinishda)")
    await Applications.next()


@dp.message_handler(state=Applications.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text
    if len(phone) != 12:
        await message.reply("Iltimos telefon raqamingizni 998901234567 ko'rinishda kirting")
        await Applications.phone.set()
        return
    await state.update_data(phone=phone)
    await message.answer("Arizangiz matnini to'liq va aniq ravishda yozing:")
    await Applications.next()


@dp.message_handler(state=Applications.application_text)
async def get_app(message: Message, state: FSMContext):
    applications_text = message.text
    await state.update_data(applications_text=applications_text, user_id=message.from_user.id,
                            message_id=message.message_id, status='pending', mention=message.from_user.get_mention())
    # await state.update_data(user_id=message.from_user.id)
    # await state.update_data(message_id=message.message_id)
    # await state.update_data(status='pending')
    # await state.update_data(mention=message.from_user.get_mention())
    data = await state.get_data()
    msg = f"Ismingiz - {data.get('first_name')}\n"
    msg += f"Familyangiz - {data.get('last_name')}\n"
    msg += f"Telefon - {data.get('phone')}\n"
    msg += f"Ariza matni - {data.get('applications_text')}\n"
    data_local.append(data)
    await message.answer(f"Arizangiz quyidagi ko'rinishda")
    await message.answer(msg + "\n<b>USHBU ARIZA TEGISHLI JOYGA YUBORILSINMI?</b>", parse_mode="HTML", reply_markup=confirmation_keyboard)
    await Applications.next()


# @dp.callback_query_handler(state=Applications.confirmation)
# async def confirmation(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#     await call.message.answer("Ushbu arizani tegishli joylarga yuborasizmi?", reply_markup=confirmation_keyboard)


@dp.callback_query_handler(confirmation_callback.filter(action="confirm"), state=Applications.confirmation)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    # async with state.proxy() as data:
    #     text = data.get("text")
    await call.message.edit_reply_markup()
    await call.message.answer("Ariza tegishli tashkilotga yuborildi")
    data = await state.get_data()
    msg = f"<b>Ismi</b> - {data.get('first_name')}\n"
    msg += f"<b>Familyasi</b> - {data.get('last_name')}\n"
    msg += f"<b>Telefoni</b> - {data.get('phone')}\n"
    msg += f"<b>Ariza matni</b> - {data.get('applications_text')}\n"
    mention = data.get("mention")
    await state.finish()
    await bot.send_message(ADMINS[0], f"Foydalanuvchi {mention} quyidagicha ariza yubordi:")
    await bot.send_message(ADMINS[0], msg, parse_mode="HTML", reply_markup=confirmation_keyboard)


@dp.callback_query_handler(confirmation_callback.filter(action="cancel"), state=Applications.confirmation)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post rad etildi.")

    @dp.message_handler(state=Applications.Confirm)
    async def post_unknown(message: Message):
        await message.answer("Yuborish etish yoki rad etishni tanlang")


async def save_data(message: Message):
    await message.answer(
        "Arizangiz muvaffaqiyatli qabul qilindi. Tez orada arizangizni ko'rib chiqib siz bilan bog'lanamiz.",
        reply_markup=start_menu)
    result = [{
        'fish': data_local[0].get('first_name') + data_local[0].get('last_name'),
        'user_id': data_local[0].get('user_id'),
        'phone_number': data_local[0].get('phone'),
        'message': data_local[0].get('applications_text'),
        'message_id': data_local[0].get('message_id'),
        'status': data_local[0].get('status'),
    }]
    # await state.finish()
    print("Sending data...")
    # r = requests.post(f'http://{IP}:8080/application', data={'applications': result})
    # print("Result: " + str(r))
    await on_startup_notify(dp, data_local[0])
    if len(data_local) > 0:
        data_local.clear()
