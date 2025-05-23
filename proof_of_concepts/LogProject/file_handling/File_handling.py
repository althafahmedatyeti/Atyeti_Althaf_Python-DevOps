import os
class FileHandler:
    import os

class FileHandler:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.log_levels = ['INFO', 'WARN', 'ERROR']
        self.log_counts = {}

    def read_and_count_logs(self):
        """
        Reads all files in the folder, counts occurrences of each log level per file.
        """
        for filename in os.listdir(self.folder_path):
            filepath = os.path.join(self.folder_path, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    lines = file.readlines()

                counts = {level: 0 for level in self.log_levels}
                for line in lines:
                    for level in self.log_levels:
                        if level in line:
                            counts[level] += 1
                self.log_counts[filename] = counts

    def get_log_counts(self):
        return self.log_counts
