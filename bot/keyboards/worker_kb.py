from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_worker_kb():
    builder = ReplyKeyboardBuilder()

    builder.button(
        text='Отправить геолокацию', request_location=True
    )

    return builder.as_markup(resize_keyboard=True)


