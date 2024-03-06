from typing import List

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.config_reader import load_config

from bot.filters.admin_filter import IsAdminFilter

config = load_config()

admin_router = Router()
admins = [int(admin) for admin in config.bot.admins]


@admin_router.message(IsAdminFilter(admins), Command('admin'))
async def admin_menu(message: Message):
    await message.answer("Обработка сообщения от /admin")
