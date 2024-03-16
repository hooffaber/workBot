from aiogram.fsm.state import StatesGroup, State


class AddUser(StatesGroup):
    add_tg_username = State()
    add_fullname = State()
    confirm_data = State()


class DeleteUser(StatesGroup):
    show_user_list = State()


class AddObject(StatesGroup):
    add_object_name = State()
    confirm_data = State()


class DeleteObject(StatesGroup):
    show_object_list = State()


class WorkerStates(StatesGroup):
    add_geo = State()
    add_object = State()
    add_work_hours = State()
    add_voice_msg = State()

    write_msg_byhands = State()
    wait_next_obj = State()

    finish_job = State()
