import os
from dataclasses import dataclass


@dataclass
class TgBot:
    bot_token: str


@dataclass
class Config:
    bot: TgBot


def load_config():
    bot_token = os.getenv('BOT_TOKEN')

    return Config(bot=TgBot(bot_token=bot_token))
