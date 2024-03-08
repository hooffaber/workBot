from typing import List
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.db.models import Base, Worker, WorkHours
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


def add_work_hour(tg_name, address) -> int:

    session = Session()

    try:
        tg_name = "@" + tg_name
        worker = session.query(Worker).filter(Worker.tg_name == tg_name).first()
        start_time = datetime.now()
        new_work_hour = WorkHours(worker=worker.tg_name, startTime=start_time, address=address)

        session.add(new_work_hour)

        session.commit()

        return new_work_hour.id

    except Exception as e:
        session.rollback()
        print("Error occurred while adding worker's start time and address:", e)

    #finally:
        #session.close()


def update_finish_time(work_hour_id) -> None:
    session = Session()

    try:
        work_hour_to_update = session.query(WorkHours).get(work_hour_id)

        if work_hour_to_update:
            work_hour_to_update.finishTime = datetime.now()

            session.commit()

        else:
            print("No work record found for the provided WorkHours entity.")

    except Exception as e:
        # Rollback the transaction in case of any error
        session.rollback()
        print("Error occurred while updating worker's finish time:", e)

   # finally:
    #    session.close()


def get_users(flag: str = 'fullname') -> List[str]:
    session = Session()
    query_result: List[Worker] = session.query(Worker).all()

    #session.close()
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
