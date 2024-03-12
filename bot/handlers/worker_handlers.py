from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from bot.location import get_location

from bot.keyboards.worker_kb import make_worker_kb, make_object_kb, make_submit_form_kb, make_start_kb
from bot.keyboards.voice_kb import instead_voice_kb
from bot.states import WorkerStates

from bot.db.orm import add_work_hour, update_finish_time, add_facility, update_finish_address

worker_router = Router()


@worker_router.callback_query(F.data == 'return_geo', WorkerStates.wait_next_obj)
async def start_cmd(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    update_finish_time(work_hour_id=data['db_entity_id'])

    await callback.message.answer('Для того, чтобы закончить работу, отправьте геолокацию',
                                  reply_markup=make_worker_kb())

    await state.set_state(WorkerStates.finish_job)


@worker_router.message(F.location, WorkerStates.finish_job)
async def wait_finish_location(message: Message, state: FSMContext):
    await message.reply("Отлично. Идёт обработка гео.", reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    db_entity_id = data['db_entity_id']
    location = get_location(long=message.location.longitude, lat=message.location.latitude)
    update_finish_address(db_entity_id, location)

    await state.clear()

    await message.answer('Работа закончена.', reply_markup=make_start_kb())


@worker_router.message(F.location, WorkerStates.add_geo)
async def get_loc(message: Message, state: FSMContext):
    await message.reply("Отлично. Идёт обработка гео.", reply_markup=ReplyKeyboardRemove())

    # location = "Село Кукуево"

    location = get_location(long=message.location.longitude, lat=message.location.latitude)

    db_entity_id: int = add_work_hour(tg_name=message.from_user.username, address=location)

    await state.update_data(address=location)
    await state.update_data(db_entity_id=db_entity_id)

    await state.set_state(WorkerStates.add_object)

    await message.answer('Теперь вы можете добавить объект', reply_markup=make_object_kb())


@worker_router.callback_query(F.data.in_(['add_object', 'return_object']))
async def add_object(callback: CallbackQuery, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state in [WorkerStates.add_work_hours, WorkerStates.add_object, WorkerStates.wait_next_obj]:
        await callback.message.edit_text('Введите название объекта:', reply_markup=None)
        await state.set_state(WorkerStates.add_object)
    else:
        return
    await callback.answer()


@worker_router.message(F.text, WorkerStates.add_object)
async def get_object(message: CallbackQuery, state: FSMContext):
    await state.update_data(object_name=message.text)
    await message.answer(f'Объект "{message.text}" добавлен.\nСколько часов вы проработали? Пример: 2.4')

    await state.set_state(WorkerStates.add_work_hours)


@worker_router.message(WorkerStates.add_work_hours)
async def get_hours(message: CallbackQuery, state: FSMContext):
    try:
        message_text: str = message.text.replace(',', '.')
        hours_quantity = float(message_text)
    except ValueError:
        await message.answer("Неверно введённое количество часов. Попробуйте снова.")
        return

    await state.update_data(wh_quantity=message_text)
    data = await state.get_data()

    await message.answer(text=f'По адресу {data["address"]}\n\n'
                              f'Вы работали на объекте "{data["object_name"]}" '
                              f'в течение {data["wh_quantity"]} часа(часов). '
                              f'Всё верно?',
                         reply_markup=make_submit_form_kb())


@worker_router.callback_query(F.data.in_(['confirm_object', 'reset_voice']))
async def confirm_obj(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отправьте голосовое сообщение с кратким описанием работы:",
                                     reply_markup=instead_voice_kb())

    await state.set_state(WorkerStates.add_voice_msg)


@worker_router.callback_query(F.data == 'submit_voice')
async def submit_full(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    address, obj_name, hours_quantity = data.get('address'), data.get('object_name'), data.get('wh_quantity')

    voice_text = data['voice_text']

    add_facility(work_hour_id=data['db_entity_id'], obj_name=obj_name, hours=hours_quantity, description=voice_text)

    # debug information
    # await callback.message.answer(f'{address, obj_name, hours_quantity, voice_text}')
    await state.set_state(WorkerStates.wait_next_obj)
    await callback.message.answer('Теперь вы можете добавить объект', reply_markup=make_object_kb())
