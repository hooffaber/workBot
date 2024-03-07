from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.filters.worker_filter import IsWorkerFilter
from bot.keyboards.worker_kb import make_worker_kb
from bot.db.orm import get_users

from bot.states import WorkerStates

default_cmd_router = Router()


@default_cmd_router.message(Command('start'), IsWorkerFilter())
async def start_cmd(message: Message, state: FSMContext):
    await message.answer('Для того, чтобы начать работу, отправьте геолокацию',
                         reply_markup=make_worker_kb())

    await state.set_state(WorkerStates.add_geo)
