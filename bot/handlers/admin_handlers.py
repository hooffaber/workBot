from typing import List

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.config_reader import load_config

from bot.filters.admin_filter import IsAdminFilter
from bot.keyboards.admin_kb import make_admin_menu
from bot.cbdata import AdminMenuCallbackFactory

config = load_config()

admin_router = Router()
admins = [int(admin) for admin in config.bot.admins]


@admin_router.message(IsAdminFilter(admins), Command('admin'))
async def admin_menu(message: Message):
    await message.answer("Панель управления", reply_markup=make_admin_menu())


@admin_router.callback_query(AdminMenuCallbackFactory.filter())
async def admin_action_cmd(callback: CallbackQuery, callback_data: AdminMenuCallbackFactory):
    action = callback_data.action
    if action == "add":
        pass
    elif action == "remove":
        pass
    else:
        pass