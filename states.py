from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    phone = State()


class Questioning(StatesGroup):
    num_emploeyes = State()
    turnover = State()
    role = State()
    asking_number = State()
