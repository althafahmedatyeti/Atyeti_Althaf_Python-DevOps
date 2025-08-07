from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), index=True)
    email = Column(String(40), index=True)
    password = Column(String(150) , index= True)
    role=Column(String(20),default="user")


