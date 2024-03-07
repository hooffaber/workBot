from aiogram.fsm.state import StatesGroup, State


class AddUser(StatesGroup):
    add_tg_username = State()
    add_fullname = State()
    confirm_data = State()


class DeleteUser(StatesGroup):
    show_user_list = State()


class WorkerStates(StatesGroup):
    add_geo = State()
    add_object = State()
    add_work_hours = State()
    add_voice_msg = State()

