from sqlalchemy import create_engine, Column, Integer, String
from database import Base
class Bus(Base):
    __tablename__= 'buses'
    bus_id=Column(Integer,primary_key=True,index=True)
    bus_source=Column(String(100),index=True)
    bus_destination=Column(String(100),index=True)
    bus_name=Column(String(100),index=True)
