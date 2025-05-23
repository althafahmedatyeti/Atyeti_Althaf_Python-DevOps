from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DTO.Error import ErrorLog
from DTO.Info import InfoLog
from DTO.Warning import WarnLog
from service.dd_config import session

class Db_service:
    def __init__(self,session):
        self.db=session
    def db_add_log_count(self,filename,log_class,count):
        try:
            entry1 = log_class(filename,count)
            self.db.add(entry1)
            self.db.commit()
            print(f"Inserted into {log_class.__tablename__}: {filename} with count {count}")
        except Exception as e :
            self.db.rollback()
            print(f"Error inserting into {log_class.__tablename__}: {e}")
    def add_info_log(self,filename,count):
        self.db_add_log_count(log_class=InfoLog,filename=filename,count=count)

    def add_warn_log(self, filename, count):
        self.db_add_log_count(log_class=WarnLog, filename=filename, count=count)

    def add_error_log(self, filename, count):
        self.db_add_log_count(log_class=ErrorLog, filename=filename, count=count)

    def close(self):
        self.db.close()


