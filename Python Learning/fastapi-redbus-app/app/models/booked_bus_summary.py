from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from database import Base
class BusBookingSummary(Base):
    __tablename__ = 'bus_booking_summary'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey('buses.bus_id'), index=True)
    source = Column(String(100))
    destination = Column(String(100))
    travel_date = Column(Date, index=True)
    booked_seats = Column(Integer, default=0)
    available_seats = Column(Integer)