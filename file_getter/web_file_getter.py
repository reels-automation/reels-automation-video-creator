import os
import requests
import uuid
from file_getter.file_getter import FileGetter

class WebImageFileGetter(FileGetter):
    def __init__(self, temp_folder: str):
        super().__init__(temp_folder)
        os.makedirs(self.temp_folder, exist_ok=True)

    def get_file(self, file_name: str, file_location: str) -> str:
        """
        Downloads an image from a URL and saves it with `file_name` in the temp folder.
        """
        response = requests.get(file_location, stream=True)
        if response.status_code == 200:
            local_path = os.path.join(self.temp_folder, file_name)
            with open(local_path, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            return local_path
        else:
            raise Exception(f"Error downloading file from {file_location}, status code: {response.status_code}")

    def get_random_file(self, file_location: str) -> str:
        """
        Downloads an image from a URL and saves it with a random name in the temp folder.
        """
        random_name = f"{uuid.uuid4().hex}.jpg"
        return self.get_file(random_name, file_location)


