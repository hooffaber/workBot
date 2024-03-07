import os.path

from aiogram import Router, Bot, F
from aiogram.enums.chat_action import ChatAction
from aiogram.types import ContentType, Message

from bot.keyboards.voice_kb import make_voice_to_text_kb
from voice_recognition.voice import speech_recognition

voice_router = Router()


# TODO: ОБЯЗАТЕЛЬНО добавить фильтр на состояние
@voice_router.message(F.voice)
async def voice_message_handler(message: Message, bot: Bot):
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

    text = speech_recognition(file_on_disk)

    if not text:
        text = "Формат документа не поддерживается"
    await loading_message.delete()
    await message.answer(text, reply_markup=make_voice_to_text_kb())

    os.remove(file_on_disk)  # Удаление временного файла
