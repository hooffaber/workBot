from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.cbdata import WorkerPickingCallbackFactory
from bot.db.orm import get_all_objects
from bot.db.models import AdminObject


def make_worker_kb():
    builder = ReplyKeyboardBuilder()

    builder.button(
        text='Отправить геолокацию', request_location=True
    )

    return builder.as_markup(resize_keyboard=True)


def make_object_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Добавить объект', callback_data='add_object'
    )
    builder.button(
        text='Завершить работу', callback_data='return_geo'
    )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def make_submit_form_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подтвердить ввод", callback_data='confirm_object'
    )
    builder.button(
        text="Ввести заново", callback_data="return_object"
    )

    builder.adjust(1)

    return builder.as_markup()


def make_start_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="/start"
    )

    return builder.as_markup(resize_keyboard=True)


def choose_obj_kb():
    builder = InlineKeyboardBuilder()

    objects: list[AdminObject] = get_all_objects(flag='full')

    for obj in objects:
        builder.button(text=obj.name, callback_data=WorkerPickingCallbackFactory(obj_id=str(obj.id)))

    builder.button(text='Обновить список объектов', callback_data='refresh_objects')

    builder.adjust(2)

    return builder.as_markup()
