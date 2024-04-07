from aiogram import Bot


async def send_notification(bot: Bot, chat_id: int, to_start: bool = True):
    if to_start:
        await bot.send_message(chat_id=chat_id,
                               text=f'Напоминание: Пора начинать рабочий день!')
    else:
        await bot.send_message(chat_id=chat_id,
                               text=f'Напоминание: Рабочий день пора заканчивать.')
