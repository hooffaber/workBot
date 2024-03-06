import os
from dataclasses import dataclass


@dataclass
class TgBot:
    bot_token: str


@dataclass
class DB:
    db_name: str

@dataclass
class Config:
    bot: TgBot
    db: DB


def load_config():
    bot_token = os.getenv('BOT_TOKEN')
    db_name = os.getenv('DB_NAME')

    return Config(bot=TgBot(bot_token=bot_token),
                  db=DB(db_name=db_name))
