from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.cbdata import AdminMenuCallbackFactory, AdminDelCallbackFactory, AdminExportFactory

from bot.db.orm import get_users, get_objects


def make_admin_menu():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Добавить сотрудника', callback_data=AdminMenuCallbackFactory(action='add', subject='worker')
    )
    builder.button(
        text='Удалить сотрудника', callback_data=AdminMenuCallbackFactory(action='remove', subject='worker')
    )
    builder.button(
        text='Добавить объект', callback_data=AdminMenuCallbackFactory(action='add', subject='object')
    )
    builder.button(
        text='Удалить объект', callback_data=AdminMenuCallbackFactory(action='remove', subject='object')
    )
    builder.button(
        text='Выгрузить отчёт', callback_data=AdminMenuCallbackFactory(action='export_data', subject='')
    )

    builder.adjust(2)

    return builder.as_markup()


def make_admin_submit_user():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Подтвердить ввод', callback_data="submit_add_user")
    )
    return builder.as_markup()


def make_admin_submit_obj():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Подтвердить ввод', callback_data="submit_add_obj")
    )
    return builder.as_markup()


def delete_user_kb():
    builder = InlineKeyboardBuilder()

    fullnames = get_users()

    for fullname in fullnames:
        builder.button(text=fullname, callback_data=AdminDelCallbackFactory(name=fullname, subject='worker'))

    builder.button(text='Вернуться назад', callback_data='main_admin_menu')

    builder.adjust(2)

    return builder.as_markup()


def delete_obj_kb():
    builder = InlineKeyboardBuilder()

    objects = get_objects()

    for obj in objects:
        builder.button(text=obj, callback_data=AdminDelCallbackFactory(name=obj, subject='object'))

    builder.button(text='Вернуться назад', callback_data='main_admin_menu')

    builder.adjust(2)

    return builder.as_markup()


def submit_deletion_kb(subject: str):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Подтвердить удаление', callback_data='submit_delete'))
    builder.button(text='Вернуться назад', callback_data=AdminMenuCallbackFactory(action='remove', subject=subject))

    builder.adjust(1)

    return builder.as_markup()


def make_export_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='За день', callback_data=AdminExportFactory(date="day"))
    builder.button(text='За месяц', callback_data=AdminExportFactory(date="month"))

    return builder.as_markup()
