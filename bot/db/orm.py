from typing import List, Any
from datetime import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

import pandas as pd

from bot.db.models import Base, Worker, WorkHours, FacilityWork, HoursFacility, AdminObject
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


def add_object(obj_name: str):
    session = Session()
    obj = session.query(AdminObject).filter(AdminObject.name == obj_name).first()
    if not obj:
        new_object = AdminObject(name=obj_name)
        session.add(new_object)
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

    except Exception as e:
        session.rollback()
        print("Error occurred while adding worker's start time and address:", e)

    return new_work_hour.id


def update_finish_time(work_hour_id) -> None:
    try:
        with Session() as session:
            work_hour_to_update = session.query(WorkHours).get(work_hour_id)

            if work_hour_to_update:
                work_hour_to_update.finishTime = datetime.now()

                session.commit()

            else:
                print("No work record found for the provided WorkHours entity.")

    except Exception as e:
        print("Error occurred while updating worker's finish time:", e)


def update_finish_address(work_hour_id, address: str) -> None:
    try:
        with Session() as session:
            work_hour_to_update = session.query(WorkHours).get(work_hour_id)

            if work_hour_to_update:
                work_hour_to_update.finish_address = address

                session.commit()

            else:
                print("No work record found for the provided WorkHours entity to update finish address.")

    except Exception as e:
        # Rollback the transaction in case of any error
        session.rollback()
        print("Error occurred while updating worker's finish address:", e)


def add_facility(work_hour_id: int, obj_name: str, hours: int, description: str):
    session = Session()

    try:

        facility = FacilityWork(objectName=obj_name, workedHours=hours, description=description)

        session.add(facility)
        session.commit()

        facility_string_id = facility.id

        work_facility_connection = HoursFacility(workHours_id=work_hour_id, facilityWork_id=facility_string_id)

        session.add(work_facility_connection)

        session.commit()

    except Exception as e:
        session.rollback()
        print("Error occurred while adding facility:", e)

    # connection_id = session.query(WorkHours).get(work_hour_id).id


def get_users(flag: str = 'fullname') -> List[str]:
    session = Session()
    query_result: List[Worker] = session.query(Worker).all()

    # session.close()
    if flag == 'tg_name':
        return [worker.tg_name for worker in query_result]

    if flag == 'fullname':
        return [worker.fullname for worker in query_result]


def get_all_objects(flag: str | None = None) -> List[str | int | AdminObject]:
    session = Session()
    query_result: List[AdminObject] = session.query(AdminObject).all()
    if not flag:
        return [obj.name for obj in query_result]
    if flag == 'id':
        return [obj.id for obj in query_result]
    if flag == 'full':
        return query_result
    else:
        raise RuntimeError(f"Неправильный flag в bot.orm.get_objects(): {flag}")


def get_obj_by_id(obj_id: int):
    session = Session()
    query_result: AdminObject = session.query(AdminObject).filter(AdminObject.id == obj_id).first()
    if query_result:
        return query_result.name
    raise RuntimeError(f"Не найдено объекта с id={obj_id}")


def delete_worker(delete_fullname: str):
    session = Session()
    user_to_delete = session.query(Worker).filter(Worker.fullname == delete_fullname).first()

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()


def delete_object(obj_name: str):
    session = Session()
    obj_to_delete = session.query(AdminObject).filter(AdminObject.name == obj_name).first()

    if obj_to_delete:
        session.delete(obj_to_delete)
        session.commit()


def export_query(export_time: str) -> Any:
    session = Session()
    try:
        now = datetime.now()
        if export_time == 'day':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            query_data = session.query(WorkHours, Worker.fullname, FacilityWork.objectName, FacilityWork.workedHours, \
                                       FacilityWork.description).join(Worker, WorkHours.worker == Worker.tg_name). \
                join(HoursFacility, WorkHours.id == HoursFacility.workHours_id). \
                join(FacilityWork, HoursFacility.facilityWork_id == FacilityWork.id). \
                filter(WorkHours.startTime >= start_date, WorkHours.startTime <= end_date).all()
        elif export_time == 'month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = start_date.replace(month=now.month % 12 + 1) if now.month < 12 else start_date.replace(
                year=now.year + 1, month=1)
            query_data = session.query(WorkHours, Worker.fullname, FacilityWork.objectName, FacilityWork.workedHours, \
                                       FacilityWork.description).join(Worker, WorkHours.worker == Worker.tg_name). \
                join(HoursFacility, WorkHours.id == HoursFacility.workHours_id). \
                join(FacilityWork, HoursFacility.facilityWork_id == FacilityWork.id). \
                filter(WorkHours.startTime >= start_date, WorkHours.startTime < next_month).all()
        else:
            print("Invalid export time specified.")
            return

    except Exception as e:
        print("Error occurred while export query:", e)
        query_data = []

    return query_data


def summarize_worked_hours():
    session = Session()

    results = session.query(
        FacilityWork.objectName,
        Worker.fullname,
        func.sum(FacilityWork.workedHours).label('total_hours')
    ).join(
        HoursFacility, HoursFacility.facilityWork_id == FacilityWork.id
    ).join(
        WorkHours, WorkHours.id == HoursFacility.workHours_id
    ).join(
        Worker, Worker.tg_name == WorkHours.worker
    ).group_by(
        FacilityWork.objectName, Worker.fullname
    ).all()

    summary = {}
    for objectName, fullname, total_hours in results:
        if objectName not in summary:
            summary[objectName] = {}
        summary[objectName][fullname] = total_hours

    return summary
