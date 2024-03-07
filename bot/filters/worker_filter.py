from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message
from bot.db.orm import get_users


class IsWorkerFilter(BaseFilter):
    async def __call__(self, message: Message):
        tg_names = [tg_name.split('@')[1] for tg_name in get_users('tg_name')]
        if not message.from_user.username:
            return False
        return message.from_user.username in tg_names
