from loader import dp
from aiogram.dispatcher import FSMContext
from states.applications import Applications
from keyboards.default.applications_finish import finish_app
from aiogram.types import Message, ReplyKeyboardRemove
from utils.notify_admins import on_startup_notify
from keyboards.default.start_keyboards import start_menu
from data.config import IP
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
    await state.update_data(applications_text=applications_text)
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(message_id=message.message_id)
    await state.update_data(status='pending')
    data = await state.get_data()
    msg = f"Ismingiz - {data.get('first_name')}\n"
    msg += f"Familyangiz - {data.get('last_name')}\n"
    msg += f"Telefon - {data.get('phone')}\n"
    msg += f"Ariza matni - {data.get('applications_text')}\n"
    data_local.append(data)
    await message.answer(f"Arizangiz quyidagi ko'rinishda:\n{msg}", reply_markup=finish_app)
    await state.finish()


async def save_data(message: Message):
    await message.answer(
        "Arizangiz muvaffaqiyatli qabul qilindi. Tez orada arizangizni ko'rib chiqib siz bilan bog'lanamiz.",
        reply_markup=start_menu)
    # data = await state.get_data()
    # result = [{
    #     'fish': data.get('first_name') + data.get('last_name'),
    #     'user_id': data.get('user_id'),
    #     'phone_number': data.get('phone'),
    #     'message': data.get('applications_text'),
    #     'message_id': data.get('message_id'),
    #     'status': data.get('status'),
    # }]
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
    r = requests.post(f'http://{IP}:8080/application', data={'applications': result})
    print("Result: " + str(r))
    await on_startup_notify(dp, data_local[0])
    if len(data_local) > 0:
        data_local.clear()

# const userData = {
#        user_id: ctx.message.from.id,
#        first_name: ctx.message.from.first_name,
#        last_name: ctx.message.from.last_name,
#        username: ctx.message.from.username,
#        language_code: ctx.message.from.language_code
#    }
