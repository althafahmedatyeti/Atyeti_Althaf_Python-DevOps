from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DTO.Error import ErrorLog
from DTO.Info import InfoLog
from DTO.Warning import WarnLog
from service.dd_config import db_config
from file_handling.File_handling import FileHandler

class Db_service:
    def __init__(self):
        self.db=db_config.session()
    def db_add_log_count(self,filename,log_class,count):
        #inserting data to DatatBase
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
    def add_data_to_db(self,log_count_data):
        for  filename,counts in log_count_data.items():
            if counts['INFO']>0:
                self.add_info_log(filename,counts["INFO"])
            if counts['WARN'] > 0:
                self.add_warn_log(filename, counts['WARN'])
            if counts['ERROR'] > 0:
                self.add_error_log(filename, counts['ERROR'])
    def close(self):
        self.db.close()


