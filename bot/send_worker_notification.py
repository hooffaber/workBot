from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def send_notification(bot: Bot, chat_id: int, to_start: bool = True):
    if to_start:
        await bot.send_message(chat_id=chat_id,
                               text=f'Напоминание: Пора начинать рабочий день!')
    else:
        await bot.send_message(chat_id=chat_id,
                               text=f'Напоминание: Рабочий день пора заканчивать.')


async def add_interval_notification(scheduler: AsyncIOScheduler, bot: Bot, chat_id: int, to_start: bool = True):
    scheduler.add_job(send_notification, 'interval', seconds=600, args=(bot, chat_id, to_start))
