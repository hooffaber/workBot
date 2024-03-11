import asyncio
import logging
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config_reader import load_config
from dotenv import load_dotenv

from bot.handlers.default_commands import default_cmd_router
from bot.handlers.admin_handlers import admin_router
from bot.handlers.voice_handlers import voice_router
from bot.handlers.worker_handlers import worker_router


load_dotenv()  # take environment variables from .env.



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token=load_config().bot.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(default_cmd_router, admin_router, voice_router, worker_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
