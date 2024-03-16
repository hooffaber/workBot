from typing import List

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.config_reader import load_config

from bot.filters.admin_filter import IsAdminFilter
from bot.keyboards.admin_kb import make_admin_menu, make_admin_submit_user, delete_user_kb, submit_deletion_kb, \
    make_export_kb, make_admin_submit_obj, delete_obj_kb
from bot.cbdata import AdminMenuCallbackFactory, AdminDelCallbackFactory, AdminExportFactory
from bot.states import AddUser, AddObject, DeleteObject, DeleteUser

from bot.db.orm import add_user, delete_worker, export_query, add_object, delete_object
from bot.db.export import export_data_to_google_sheets

config = load_config()

admin_router = Router()
admins = [int(admin) for admin in config.bot.admins]


@admin_router.message(IsAdminFilter(admins), Command('admin'))
async def admin_menu(message: Message):
    await message.answer("Панель управления", reply_markup=make_admin_menu())


@admin_router.callback_query(AdminMenuCallbackFactory.filter())
async def admin_action_cmd(callback: CallbackQuery, callback_data: AdminMenuCallbackFactory, state: FSMContext):
    action = callback_data.action
    subject = callback_data.subject

    if action == 'add':
        if subject == 'worker':
            await callback.message.edit_text("Введите @username работника", reply_markup=None)
            await state.set_state(AddUser.add_tg_username)

        elif subject == 'object':
            await callback.message.edit_text("Введите название объекта для добавления", reply_markup=None)
            await state.set_state(AddObject.add_object_name)
        else:
            raise RuntimeError("Не хватает subject в AdminMenuCallbackFactory")

    elif action == 'remove':
        if subject == 'worker':
            await callback.message.edit_text('Выберите работника для удаления', reply_markup=delete_user_kb())
        elif subject == 'object':
            await callback.message.edit_text('Выберите объект для удаления', reply_markup=delete_obj_kb())
        else:
            raise RuntimeError("Не хватает subject в AdminMenuCallbackFactory")

    else:
        await callback.message.edit_text('Выберите формат отчёта', reply_markup=make_export_kb())

    await callback.answer()


@admin_router.callback_query(AdminExportFactory.filter())
async def get_export(callback: CallbackQuery, callback_data: AdminExportFactory):
    data = export_query(callback_data.date)
    export_link = export_data_to_google_sheets(query_data=data,
                                               export_time=callback_data.date,
                                               spreadsheet_name=str(callback_data.date),
                                               worksheet_name=str(callback_data.date))

    await callback.message.answer(export_link)

    await callback.message.delete()

    admin_kb = [[KeyboardButton(text='/admin')]]

    await callback.message.answer(text='Для возврата панели нажмите на кнопку',
                                  reply_markup=ReplyKeyboardMarkup(keyboard=admin_kb, resize_keyboard=True))

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
        reply_markup=make_admin_submit_user())


@admin_router.callback_query(F.data == 'submit_add_user')
async def submit_user_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Вы добавили юзера', reply_markup=None
    )

    data = await state.get_data()
    tg_name, fullname = data['tg_name'], data['fullname']
    add_user(tg_name, fullname)

    await state.clear()
    await callback.message.answer("Панель управления", reply_markup=make_admin_menu())


@admin_router.message(AddObject.add_object_name)
async def input_fullname(message: Message, state: FSMContext):
    await state.update_data(obj_name=message.text)
    await message.answer(
        f'Название объекта: {message.text}\n\nЕсли ошиблись в написании названия, отправьте его ещё раз.',
        reply_markup=make_admin_submit_obj())


@admin_router.callback_query(F.data == 'submit_add_obj')
async def submit_user_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Вы добавили объект.', reply_markup=None
    )

    data = await state.get_data()
    obj_name = data['obj_name']
    print(obj_name)
    add_object(obj_name=obj_name)

    await state.clear()
    await callback.message.answer("Панель управления", reply_markup=make_admin_menu())


@admin_router.callback_query(AdminDelCallbackFactory.filter())
async def del_user_click(callback: CallbackQuery, callback_data: AdminDelCallbackFactory, state: FSMContext):
    subject = callback_data.subject
    await state.update_data(subject=subject)

    if subject == 'worker':
        await state.update_data(delete_fullname=callback_data.name)

    else:
        await state.update_data(delete_obj_name=callback_data.name)

    await callback.message.edit_text(f"Вы точно хотите удалить {callback_data.name}?",
                                     reply_markup=submit_deletion_kb(callback_data.subject))


@admin_router.callback_query(F.data == 'submit_delete')
async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['subject'] == 'worker':
        delete_fullname = data['delete_fullname']
        delete_worker(delete_fullname)
        await callback.message.edit_text('Работник удалён.', reply_markup=delete_user_kb())
    else:
        delete_obj_name = data['delete_obj_name']
        delete_object(delete_obj_name)
        await callback.message.edit_text('Объект удалён.', reply_markup=delete_user_kb())
    await state.clear()
    await callback.answer()


@admin_router.callback_query(F.data == 'main_admin_menu')
async def c(callback: CallbackQuery):
    await callback.message.edit_text("Панель управления", reply_markup=make_admin_menu())
