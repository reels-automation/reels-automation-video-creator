from abc import ABC

class FileGetter(ABC):
    def __init__(self, temp_folder: str):
        self.temp_folder = temp_folder
    
    def get_file(self,file_name:str, file_location:str)-> str:
        """Gets a file from a repository 

        Args:
            file_name (str): The name of the file that we need
            file_folder (str): The location to look for the file. A folder, a bucket, a url, etc. 

        Returns:
            str: local path where the image will be downloaded.
        """
    
    def get_random_file(self, file_location:str)->str:
        """Returns a random file from a repository (file_location)
        Returns:
            str: 
        """

    def upload_file(self):
        """Saves the file into a temp folder
        """