from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.cbdata import AdminMenuCallbackFactory, AdminDelCallbackFactory

from bot.db.orm import get_users_fullname


def make_admin_menu():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Добавить сотрудника', callback_data=AdminMenuCallbackFactory(action='add')
    )
    builder.button(
        text='Удалить сотрудника', callback_data=AdminMenuCallbackFactory(action='remove')
    )
    builder.button(
        text='Выгрузить отчёт', callback_data=AdminMenuCallbackFactory(action='export')
    )

    builder.adjust(2)

    return builder.as_markup()


def make_admin_submit():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Подтвердить ввод', callback_data="submit_add")
    )
    return builder.as_markup()


def delete_user_kb():
    builder = InlineKeyboardBuilder()

    fullnames = get_users_fullname()

    for fullname in fullnames:
        builder.button(text=fullname, callback_data=AdminDelCallbackFactory(fullname=fullname))

    builder.adjust(2)

    return builder.as_markup()


def submit_deletion_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Подтвердить удаление', callback_data='submit_delete'))
    builder.button(text='Вернуться назад', callback_data=AdminMenuCallbackFactory(action='remove'))

    builder.adjust(1)

    return builder.as_markup()
