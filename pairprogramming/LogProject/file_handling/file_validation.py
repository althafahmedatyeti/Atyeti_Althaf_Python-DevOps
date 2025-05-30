import os
import shutil
import zipfile
from datetime import datetime

class LogFileProcessor:
    def __init__(self, source_path,destination_path):
        self.source_path = source_path
        self.destination_path = destination_path
        self.valid_files = []
    def process(self):
        if not os.path.isdir(self.source_path):
            raise FileNotFoundError(f"Folder path does not exist: {self.source_path}")
        for filename in os.listdir(self.source_path):
            full_path = os.path.join(self.source_path, filename)
            if filename.lower().endswith(".zip"):
                self._extract_zip(full_path)
        for filename in os.listdir(self.source_path):
            if filename.lower().endswith(".txt"):
                full_path = os.path.join(self.source_path, filename)
                if self.file_validate(full_path):
                    self.valid_files.append(full_path)
                    if self.destination_path:
                        shutil.copy(full_path,self.destination_path)#move to move files
                    else:
                        print("No destination_path")
        return self.valid_files

    def _extract_zip(self, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.source_path)
                print(f"Extracted: {zip_path}")
        except zipfile.BadZipFile:
            print(f"Invalid zip file: {zip_path}")

    def file_validate(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.read().strip().split('\n') #lines stores all data in list format
            if len(lines)<3:
                return False
            header = lines[0]
            if ',' not in header:
                return False
            name_part, date_part = header.split(',')
            if not name_part.endswith(".txt"):
                return False
            try:
                date_str = date_part.strip()
                datetime.strptime(date_str, "%Y-%m-%d")
            except:
                return False
            try:
                expected_count = int(lines[-1])
                actual_count = len(lines) - 2
                if expected_count != actual_count:
                    return False
            except:
                return False
            return True
        except Exception as e:
            print(f"Error in validating file {filepath}: {e}")
            return False




