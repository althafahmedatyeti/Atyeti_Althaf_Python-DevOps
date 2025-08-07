from sqlalchemy import Column ,String,Integer
from database import Base
class Admin(Base):
    __tablename__='admin'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(30), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    role = Column(String(20), default="admin")
    