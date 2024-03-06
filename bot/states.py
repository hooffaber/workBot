from aiogram.fsm.state import StatesGroup, State


class AddUser(StatesGroup):
    add_tg_username = State()
    add_fullname = State()
    confirm_data = State()


class DeleteUser(StatesGroup):
    show_user_list = State()
