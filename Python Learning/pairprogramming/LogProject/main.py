import time

from service.JSON_Writer import JSON_Writer
# from file_handling.file_validation import destination_path
from service.dd_config import db_config
from DTO.Info import InfoLog
from DTO.Warning import WarnLog
from DTO.Error import ErrorLog
from DTO.Info import Base
# from service.dd_config import session
from service.Db_service import Db_service
from file_handling.file_validation import LogFileProcessor
from file_handling.File_handling import FileHandler
def main():
    start_time = time.time()
    Base.metadata.create_all(bind=db_config.engine)
    # db_session = db_config.session()
    service = Db_service()
    folder_path="C:\\Users\\MohammedAlthafAhmed\\IdeaProjects\\LogProject\\input_files"
    destination_path="C:\\Users\\MohammedAlthafAhmed\\IdeaProjects\\LogProject\\source"
    output_path="C:\\Users\\MohammedAlthafAhmed\\IdeaProjects\\LogProject\\Output_files"
    file_validation_obj=LogFileProcessor(folder_path,destination_path)
    file_validation_obj.process()
    file_handler_obj=FileHandler(destination_path)
    file_handler_obj.read_and_process_logs()
    log_count_data=file_handler_obj.get_log_counts()
    log_data =file_handler_obj.get_json_data()
    service.add_data_to_db(log_count_data)
    service.close()
    json_output_obj=JSON_Writer(output_path)
    print(log_data)
    json_output_obj.json_files_writer(log_data)
    end_time=time.time()
    print(f"Execution Time{end_time-start_time:.4f}")
    file_handler_obj.del_input_files(folder_path)
    file_handler_obj.del_input_files(destination_path)
if __name__ == "__main__":
    main()




