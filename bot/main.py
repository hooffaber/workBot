import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config_reader import load_config

from bot.handlers.default_commands import default_cmd_router
from bot.handlers.admin_handlers import admin_router
from bot.handlers.voice_handlers import voice_router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token=load_config().bot.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(default_cmd_router, admin_router, voice_router)

    await dp.start_polling(bot)


asyncio.run(main())
