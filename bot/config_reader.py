import os
from dataclasses import dataclass


@dataclass
class TgBot:
    bot_token: str
    admins: list[str]
    model_mode: str


@dataclass
class DB:
    db_name: str


@dataclass
class Config:
    bot: TgBot
    db: DB


def load_config():
    bot_token = os.environ.get('BOT_TOKEN')
    admins = os.environ.get('ADMINS').split(',')
    db_name = os.environ.get('DB_NAME')
    model_voice = os.environ.get('MODEL_MODE')

    return Config(bot=TgBot(bot_token=bot_token, admins=admins, model_mode=model_voice),
                  db=DB(db_name=db_name))
