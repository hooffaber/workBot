from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.db.models import Base, Worker
from bot.config_reader import load_config

config = load_config()
db_name = config.db.db_name

db_url = f'sqlite:///{db_name}.db'
engine = create_engine(db_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_user(tg_name: str, fullname: str):
    session = Session()
    user = session.query(Worker).filter(Worker.tg_name == tg_name).first()
    if not user:
        new_worker = Worker(tg_name=tg_name, fullname=fullname)
        session.add(new_worker)
        session.commit()



def get_users(flag: str = 'fullname') -> List[str]:
    session = Session()
    query_result: List[Worker] = session.query(Worker).all()

    session.close()
    if flag == 'tg_name':
        return [worker.tg_name for worker in query_result]

    if flag == 'fullname':
        return [worker.fullname for worker in query_result]


def delete_worker(delete_fullname: str):
    session = Session()
    user_to_delete = session.query(Worker).filter(Worker.fullname == delete_fullname).first()

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()

