import os.path

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_action import ChatAction
from aiogram.types import ContentType, Message, CallbackQuery

from bot.keyboards.voice_kb import make_voice_to_text_kb
from voice_recognition.voice import speech_recognition

from bot.states import WorkerStates

from bot.config_reader import load_config

config = load_config()
model_mode = config.bot.model_mode

voice_router = Router()


@voice_router.message(F.voice, WorkerStates.add_voice_msg)
async def voice_message_handler(message: Message, bot: Bot, state: FSMContext):
    """
    Обработчик на получение голосового и аудио сообщения.
    """
    if message.content_type == ContentType.VOICE:
        file_id = message.voice.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    file = await bot.get_file(file_id)
    file_path = file.file_path

    if not os.path.exists('data/tmp/'):
        os.makedirs('data/tmp/')

    file_on_disk = os.path.join("", f"data/tmp/{file_id}.mp3")

    await bot.download_file(file_path, destination=file_on_disk)
    loading_message = await message.answer("Аудио получено. Подождите, идёт обработка...")

    await bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)

    text = speech_recognition(file_on_disk, model=model_mode)
    await state.get_data()
    await state.update_data(voice_text=text)

    if not text:
        text = "Формат документа не поддерживается"
    await loading_message.delete()
    await message.answer(text, reply_markup=make_voice_to_text_kb())

    os.remove(file_on_disk)  # Удаление временного файла


@voice_router.callback_query(F.data == 'text_byhands', WorkerStates.add_voice_msg)
async def write_msg_byhands(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите сообщение с клавиатуры:")

    await state.set_state(WorkerStates.write_msg_byhands)
    await callback.answer()


@voice_router.message(WorkerStates.write_msg_byhands)
async def catch_written_msg(message: Message, state: FSMContext):
    await state.set_state(WorkerStates.add_voice_msg)
    await state.update_data(voice_text=message.text)

    await message.answer(message.text, reply_markup=make_voice_to_text_kb())