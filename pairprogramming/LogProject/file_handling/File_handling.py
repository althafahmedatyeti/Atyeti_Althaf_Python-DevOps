import os
import threading
from datetime import datetime

class FileHandler:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.log_levels = ['INFO', 'WARN', 'ERROR']
        self.log_counts = {}  # filename -> level counts
        self.log_data = {}    # filename -> full structured data
        self.lock = threading.Lock()

    def process_file(self, filename):
        filepath = os.path.join(self.folder_path, filename)
        if not os.path.isfile(filepath):
            return


        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"Error reading file '{filename}': {e}")
            return
        level_messages = {"info": [], "warn": [], "error": []}
        counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
        for line in lines:
            parts = line.split()
            if len(parts) < 3:
                continue
            level = parts[2].upper()
            if level in counts:
                counts[level] += 1
                message = " ".join(parts[4:])  # assuming consistent format
                level_messages[level.lower()].append(message)

        structured_data = {
            "file_name": filename,
            "date_of_creation": datetime.now().strftime("%Y%m%d%H%M%S"),
            "log_levels": {
                level: {
                    "messages": msgs,
                    "count": len(msgs)
                } for level, msgs in level_messages.items()
            }
        }

        with self.lock:
            self.log_counts[filename] = counts
            self.log_data[filename] = structured_data

    def read_and_process_logs(self):
        if not os.path.isdir(self.folder_path):
            raise FileNotFoundError(f"Folder path does not exist: {self.folder_path}")

        threads = []
        for filename in os.listdir(self.folder_path):
            thread = threading.Thread(target=self.process_file, args=(filename,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        print("-------------------------------------------")
        print("DEBUG Filenames processed:", list(self.log_counts.keys()))

    def get_log_counts(self):
        return self.log_counts #return log_count

    def get_json_data(self):
        return self.log_data  # return all structured logs
    def delete_input_files(self,input_folder):
        try:
            if os.path.exists(input_folder):
                for files in os.listdir(input_folder):
                    file_path=os.path.join(input_folder,files)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        except Exception as e:
            print(e)




#
# import os
#
# class FileHandler:
#     def __init__(self, folder_path):
#         self.folder_path = folder_path
#         self.log_levels = ['INFO', 'WARN', 'ERROR']
#         self.log_counts = {}
#         self.lines_list=[]
#     def read_and_count_logs(self):
#
#         #Reads all files in the folder, counts occurrences of each log level per file.
#
#         if not os.path.isdir(self.folder_path):
#             raise FileNotFoundError(f"Folder path does not exist: {self.folder_path}")
#
#         for filename in os.listdir(self.folder_path):
#             filepath = os.path.join(self.folder_path, filename)
#             if os.path.isfile(filepath):
#                 try:
#                     with open(filepath, 'r', encoding='utf-8') as file:
#                         lines = file.readlines()
#                         self.lines_list.append(lines.strip())
#                 except Exception as e:
#                     print(f"Error reading file '{filename}': {e}")
#                     continue
#
#                 counts = {level: 0 for level in self.log_levels}
#                 for line in lines:
#                     for level in self.log_levels:
#                         if level in line:
#                             counts[level] += 1
#                 self.log_counts[filename] = counts

    # def get_log_counts(self):
    #     return self.log_counts
    # def get_log_data(self):
    #     return self.lines_list

