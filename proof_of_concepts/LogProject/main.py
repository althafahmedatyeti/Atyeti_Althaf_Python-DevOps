from service.dd_config import engine
from DTO.Info import InfoLog
from DTO.Warning import WarnLog
from DTO.Error import ErrorLog
from DTO.Info import Base
from service.dd_config import session
from service.Db_service import Db_service
from file_handling.File_handling import FileHandler
def main():
    Base.metadata.create_all(bind=engine)
    db_session = session()
    service = Db_service(db_session)
    folder_path="C:\\Users\\MohammedAlthafAhmed\\IdeaProjects\\LogProject\\source"
    file_handler_obj=FileHandler(folder_path)
    p=file_handler_obj.read_and_count_logs()
    print("-------------------------------------------")
    print(p)
    for  filename,counts in file_handler_obj.get_log_counts().items():
        if counts['INFO']>0:
            service.add_info_log(filename,counts["INFO"])
        if counts['WARN'] > 0:
            service.add_warn_log(filename, counts['WARN'])
        if counts['ERROR'] > 0:
            service.add_error_log(filename, counts['ERROR'])
    service.close()
if __name__ == "__main__":
    main()




