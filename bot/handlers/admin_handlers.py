from typing import List

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.config_reader import load_config

from bot.filters.admin_filter import IsAdminFilter
from bot.keyboards.admin_kb import make_admin_menu, make_admin_submit, delete_user_kb, submit_deletion_kb
from bot.cbdata import AdminMenuCallbackFactory, AdminDelCallbackFactory
from bot.states import AddUser, DeleteUser

from bot.db.orm import add_user, delete_worker

config = load_config()

admin_router = Router()
admins = [int(admin) for admin in config.bot.admins]


@admin_router.message(IsAdminFilter(admins), Command('admin'))
async def admin_menu(message: Message):
    await message.answer("Панель управления", reply_markup=make_admin_menu())


@admin_router.callback_query(AdminMenuCallbackFactory.filter())
async def admin_action_cmd(callback: CallbackQuery, callback_data: AdminMenuCallbackFactory, state: FSMContext):
    action = callback_data.action
    if action == "add":
        await callback.message.edit_text("Введите @username работника", reply_markup=None)
        await state.set_state(AddUser.add_tg_username)
    elif action == "remove":
        await callback.message.edit_text('Выберите работника для удаления', reply_markup=delete_user_kb())
    else:
        pass

    await callback.answer()


@admin_router.message(AddUser.add_tg_username)
async def input_username(message: Message, state: FSMContext):
    entities = message.entities or []

    mentions = []
    for item in entities:
        if item.type == 'mention':
            mentions.append(item.extract_from(message.text))

    if not mentions or len(mentions) > 1:
        await message.reply(text="Неправильный формат ввода. Нужно писать так:\n@durov\nПопробуйте снова.")
        return

    if len(mentions[0]) != len(message.text):
        await message.reply(text="Неправильный формат ввода. Нужно писать так:\n@durov\nПопробуйте снова.")
        return

    await state.update_data(tg_name=message.text)
    await message.answer(f'Логин работника {message.text}. Теперь введите его ФИО:')

    await state.set_state(AddUser.add_fullname)


@admin_router.message(AddUser.add_fullname)
async def input_fullname(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_name = data['tg_name']
    await state.update_data(fullname=message.text)
    await message.answer(
        f'Логин работника {tg_name}\nФИО работника: {message.text}\n\nЕсли ошиблись в написании ФИО, отправьте его ещё раз.',
        reply_markup=make_admin_submit())


@admin_router.callback_query(F.data == 'submit_add')
async def submit_user_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Вы добавили юзера', reply_markup=None
    )

    data = await state.get_data()
    tg_name, fullname = data['tg_name'], data['fullname']
    add_user(tg_name, fullname)

    await state.clear()
    await callback.message.answer("Панель управления", reply_markup=make_admin_menu())


@admin_router.callback_query(AdminDelCallbackFactory.filter())
async def del_user_click(callback: CallbackQuery, callback_data: AdminDelCallbackFactory, state: FSMContext):
    await state.update_data(delete_fullname=callback_data.fullname)

    await callback.message.edit_text(f"Вы точно хотите удалить {callback_data.fullname}?",
                                     reply_markup=submit_deletion_kb())


@admin_router.callback_query(F.data == 'submit_delete')
async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    delete_fullname = data['delete_fullname']
    delete_worker(delete_fullname)

    await callback.message.edit_text('Работник удалён.', reply_markup=delete_user_kb())
    await callback.answer()
