from sqlalchemy import Column, Integer, TIMESTAMP, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from bot.db.base import Base


class Worker(Base):
    __tablename__ = 'Worker'

    tg_name = Column(String, primary_key=True)
    fullname = Column(String, nullable=False)


class WorkHours(Base):
    __tablename__ = 'WorkHours'

    id = Column(Integer, primary_key=True, autoincrement=True)
    worker = Column(String, ForeignKey('Worker.tg_name'))
    startTime = Column(TIMESTAMP, nullable=False)
    finishTime = Column(TIMESTAMP)
    address = Column(Text, nullable=False)

    worker_ref = relationship("Worker", backref="workhours")


class FacilityWork(Base):
    __tablename__ = 'FacilityWork'

    id = Column(Integer, primary_key=True, autoincrement=True)
    objectName = Column(String, nullable=False)
    workedHours = Column(Float, nullable=False)
    description = Column(Text, nullable=False)


class HoursFacility(Base):
    __tablename__ = 'HoursFacility'

    workHours_id = Column(Integer, ForeignKey('WorkHours.id'), primary_key=True)
    facilityWork_id = Column(Integer, ForeignKey('FacilityWork.id'), primary_key=True)

    workHours_ref = relationship("WorkHours", backref="hoursfacility")
    facilityWork_ref = relationship("FacilityWork", backref="hoursfacility")
