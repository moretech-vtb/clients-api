from sqlalchemy import Column, String, Integer, Float, DateTime, text, func, Boolean, ForeignKey

from utils import database


class Office(database.Model):
    __tablename__ = 'offices'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    status = Column(String, nullable=False)
    rko = Column(String, nullable=False)
    office_type = Column(String, nullable=False)
    sale_point_format = Column(String, nullable=False)
    suo_availability = Column(Boolean, nullable=False)
    has_ramp = Column(Boolean, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    metro_station = Column(String)
    distance = Column(Integer, nullable=False)
    kep = Column(Boolean, nullable=False)
    my_branch = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class OpenHour(database.Model):
    __tablename__ = 'open_hours'

    id = Column(Integer, primary_key=True)
    office_id = Column(Integer, ForeignKey('offices.id'))
    day_of_week = Column(String, nullable=False)
    hours = Column(String, nullable=False)
    is_individual = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class DailyLoad(database.Model):
    __tablename__ = 'daily_load'

    id = Column(Integer, primary_key=True)
    office_id = Column(Integer, ForeignKey('offices.id'))
    day_of_week = Column(String(10), nullable=False)
    load_level = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

