import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config_reader import load_config

from bot.handlers.default_commands import default_cmd_router
from bot.handlers.admin_handlers import admin_router
from bot.handlers.voice_handlers import voice_router
from bot.handlers.worker_handlers import worker_router
from bot.middlewares.scheduler import SchedulerMiddleware


async def main():
    scheduler = AsyncIOScheduler()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token=load_config().bot.bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(SchedulerMiddleware(scheduler=scheduler))

    dp.include_routers(default_cmd_router, admin_router, voice_router, worker_router)

    scheduler.start()
    await dp.start_polling(bot)


asyncio.run(main())
