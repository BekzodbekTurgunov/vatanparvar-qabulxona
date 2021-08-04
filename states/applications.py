from aiogram.dispatcher.filters.state import State, StatesGroup


class Applications(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    application_text = State()