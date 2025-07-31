from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), index=True)
    email = Column(String(40), index=True)
    password = Column(String(150) , index= True)


# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base
# Base= declarative_base()
# class Bookings(Base):
#     __tablename__ = 'bookings'
#     booking_id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, index=True)
#     bus_id = Column(Integer, index=True)
#     seat_number = Column(Integer, index=True)
#     travel_date = Column(String(40), index=True)
