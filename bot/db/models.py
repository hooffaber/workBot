from sqlalchemy import Column, Integer, TIMESTAMP, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from bot.db.base import Base


class Worker(Base):
    """
    Таблица с @username и ФИО работников
    """
    __tablename__ = 'Worker'

    tg_name = Column(String, primary_key=True)
    fullname = Column(String, nullable=False)


class WorkHours(Base):
    """
    Таблица с @username из Worker, началом рабочего дня (2024-03-08 15:30:00), его окончанием и адресом работы.
    """
    __tablename__ = 'WorkHours'

    id = Column(Integer, primary_key=True, autoincrement=True)
    worker = Column(String, ForeignKey('Worker.tg_name'))
    startTime = Column(TIMESTAMP, nullable=False)
    finishTime = Column(TIMESTAMP)
    address = Column(Text, nullable=False)
    finish_address = Column(Text)

    worker_ref = relationship("Worker", backref="workhours")


class FacilityWork(Base):
    """
    Таблица с названием рабочего объекта, которые обходит работник во время дня, количеством проведенных на нем (объекте) часов и описание работы на объекте.
    """
    __tablename__ = 'FacilityWork'

    id = Column(Integer, primary_key=True, autoincrement=True)
    objectName = Column(String, nullable=False)
    workedHours = Column(Float, nullable=False)
    description = Column(Text, nullable=False)


class HoursFacility(Base):
    """
    Таблица для связи многие-ко-многим (Адреса и объекты)
    """
    __tablename__ = 'HoursFacility'

    workHours_id = Column(Integer, ForeignKey('WorkHours.id'), primary_key=True)
    facilityWork_id = Column(Integer, ForeignKey('FacilityWork.id'), primary_key=True)

    workHours_ref = relationship("WorkHours", backref="hoursfacility")
    facilityWork_ref = relationship("FacilityWork", backref="hoursfacility")
