from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from geopy.geocoders import Nominatim

from bot.keyboards.worker_kb import make_worker_kb, make_object_kb, make_submit_form_kb
from bot.states import WorkerStates

from bot.db.orm import add_work_hour, update_finish_time
from bot.db.models import WorkHours

worker_router = Router()


@worker_router.callback_query(F.data == 'return_geo')
async def start_cmd(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Для того, чтобы начать работу, отправьте геолокацию',
                                  reply_markup=make_worker_kb())

    await state.set_state(WorkerStates.add_geo)


@worker_router.message(F.location, WorkerStates.add_geo)
async def get_loc(message: Message, state: FSMContext):
    long = message.location.longitude
    lat = message.location.latitude

    #TODO: uncomment this
    #geolocator = Nominatim(user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0")
    #location = geolocator.reverse(f'{lat}, {long}')

    location = "Село Кукуево"

    db_entity: WorkHours = add_work_hour(message.from_user.username, location)

    await state.update_data(address=location, db_entity=db_entity)
    await state.set_state(WorkerStates.add_object)

    await message.answer('Теперь вы можете добавить объект', reply_markup=make_object_kb())


@worker_router.callback_query(F.data.in_(['add_object', 'return_object']))
async def add_object(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите название объекта:', reply_markup=None)

    await state.set_state(WorkerStates.add_object)
    await callback.answer()


@worker_router.message(F.text, WorkerStates.add_object)
async def get_object(message: CallbackQuery, state: FSMContext):
    await state.update_data(object_name=message.text)
    await message.answer(f'Объект "{message.text}" добавлен.\nСколько часов вы проработали?')

    await state.set_state(WorkerStates.add_work_hours)


@worker_router.message(WorkerStates.add_work_hours)
async def get_hours(message: CallbackQuery, state: FSMContext):
    try:
        message_text : str = message.text.replace(',', '.')
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
    await callback.message.edit_text("Отправьте голосовое сообщение с кратким описанием работы:", reply_markup=None)

    await state.set_state(WorkerStates.add_voice_msg)


@worker_router.callback_query(F.data == 'submit_voice')
async def submit_full(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    address, obj_name, hours_quantity = data.get('address'), data.get('object_name'), data.get('wh_quantity')

    voice_text = data['voice_text']

    update_finish_time(data['db_entity'])

    # debug information
    # await callback.message.answer(f'{address, obj_name, hours_quantity, voice_text}')
    await callback.message.answer('Теперь вы можете добавить объект', reply_markup=make_object_kb())
