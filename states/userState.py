from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    title = State()
    select_id = State()
    question = State()


class PersonalData(StatesGroup):
    name = State()
    email = State()
    password = State()

class GroupState(StatesGroup):
    add_group = State()
    send_group = State()

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_phone = State()
