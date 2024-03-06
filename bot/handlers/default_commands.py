from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

default_cmd_router = Router()


@default_cmd_router.message(Command('start'))
async def start_cmd(message: Message):
    await message.answer('Обработка /start')



