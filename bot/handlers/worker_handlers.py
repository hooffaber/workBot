from aiogram import Router, F
from aiogram.types import Message
from geopy.geocoders import Nominatim

from bot.states import WorkerStates
worker_router = Router()


@worker_router.message(F.location, WorkerStates.add_geo)
async def get_loc(message: Message):
    long = message.location.longitude
    lat = message.location.latitude

    geolocator = Nominatim(user_agent="workBot")
    location = geolocator.reverse(f'{lat}, {long}')

    await message.answer(f"{location.address}")