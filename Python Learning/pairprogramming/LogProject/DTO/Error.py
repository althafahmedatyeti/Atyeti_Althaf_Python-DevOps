from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from DTO.base import Base

class ErrorLog(Base):
    __tablename__ = "ERROR_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    count = Column(Integer, nullable=False)

    def __init__(self, filename, count):
        self.filename = filename
        self.count = count
