from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdminFilter(BaseFilter):
    def __init__(self, admins: List[int]):
        self.admins = admins

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins
