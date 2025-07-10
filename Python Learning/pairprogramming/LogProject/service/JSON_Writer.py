import json

from file_handling.File_handling import FileHandler
import os
class JSON_Writer:
    def __init__(self,output_folder):
        self.output_folder=output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    def json_files_writer(self,log_data):
        for filename,content in log_data.items():
            json_filename=filename.replace(".txt",'.json')
            output_path=os.path.join(self.output_folder,json_filename)
            try:
                with open(output_path ,'w' ,encoding='utf-8')as f:
                    json.dump(content, f,indent=4)
                print(f"JSON data written to: {output_path}")
            except Exception as e:
                print(f"Failed to write {json_filename}: {e}")
