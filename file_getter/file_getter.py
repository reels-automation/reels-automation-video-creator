from abc import ABC

class FileGetter(ABC):
    def __init__(self, temp_folder: str):
        self.temp_folder = temp_folder
    
    def get_file_temp_folder(self):
        """Gets a file from a repository
        """

    def upload_file(self):
        """Saves the file into a temp folder
        """