from loader import dp
from aiogram.dispatcher import FSMContext
from states.applications import Applications
from keyboards.default.applications_finish import finish_app
from aiogram.types import Message, ReplyKeyboardRemove
from utils.notify_admins import on_startup_notify

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
        reply_markup=ReplyKeyboardRemove())
    await on_startup_notify(dp, data_local[0])
    if len(data_local) > 0:
        print(data_local)
        data_local.clear()
