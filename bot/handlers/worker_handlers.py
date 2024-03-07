from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from geopy.geocoders import Nominatim

from bot.keyboards.worker_kb import make_worker_kb, make_object_kb
from bot.states import WorkerStates

worker_router = Router()


@worker_router.callback_query(F.data == 'return_geo')
async def start_cmd(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Для того, чтобы начать работу, отправьте геолокацию',
                                  reply_markup=make_worker_kb())

    await state.set_state(WorkerStates.add_geo)


@worker_router.message(F.location, WorkerStates.add_geo)
async def get_loc(message: Message, state: FSMContext):
    long = message.location.longitude
    lat = message.location.latitude

    geolocator = Nominatim(user_agent="workBot")
    location = geolocator.reverse(f'{lat}, {long}')

    await state.update_data(address=location)

    await message.answer('Теперь вы можете добавить объект', reply_markup=make_object_kb())
