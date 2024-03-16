from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_voice_to_text_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Ввести вручную', callback_data='text_byhands')
    )

    builder.add(
        InlineKeyboardButton(text='Перезаписать', callback_data='reset_voice'),
    )

    builder.add(
        InlineKeyboardButton(text='Подтвердить', callback_data='submit_voice'),
    )

    builder.adjust(2)

    return builder.as_markup()


def instead_voice_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text='Ввести вручную', callback_data='text_byhands')
    )

    return builder.as_markup()
