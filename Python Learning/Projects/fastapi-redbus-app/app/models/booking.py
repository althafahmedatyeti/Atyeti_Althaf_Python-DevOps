from sqlalchemy import create_engine, Column, Integer, String
from database import Base
class Bookings(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    bus_id = Column(Integer, index=True)
    seat_number = Column(Integer, index=True)
    travel_date = Column(String(40), index=True)
