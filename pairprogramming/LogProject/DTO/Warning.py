from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from DTO.base import Base

class WarnLog(Base):
    __tablename__ = "WARN_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    count = Column(Integer, nullable=False)

    def __init__(self, filename, count):
        self.filename = filename
        self.count = count
