from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_voice_to_text_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Подтвердить', callback_data='submit_voice'),
    )
    builder.add(
        InlineKeyboardButton(text='Перезаписать', callback_data='reset_voice'),
    )

    return builder.as_markup()