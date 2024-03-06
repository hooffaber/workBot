from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.cbdata import AdminMenuCallbackFactory


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
