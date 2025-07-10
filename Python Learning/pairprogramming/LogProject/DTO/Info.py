from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from DTO.base import  Base

class InfoLog(Base):
    __tablename__ = 'INFO_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    count = Column(Integer, nullable=False)

    def __init__(self, filename, count):
        self.filename = filename
        self.count = count
    def __repr__(self):
        return f"<Info(id={self.id}, filename='{self.filename}', level_type='{self.level_type}', count={self.count})>"




