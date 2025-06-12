import os
import requests
from minio import Minio
from minio.error import S3Error
from file_getter.file_getter import FileGetter
from settings import ADMIN_API

class FileGetterPublicMinio(FileGetter):    
    def __init__(self):
        self.temp_folder = "temp_storage_minio_public"
        self.api = ADMIN_API

    def get_random_file(self, character_name:str):
        try:
            url = f"http://{self.api}/random-image/{character_name}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            object_name = data["object_name"]
            object_url = data["object_url"]
            file_response = requests.get(object_url)
            file_response.raise_for_status()
            local_path = os.path.join(self.temp_folder, object_name)
            with open(local_path, "wb") as f:
                f.write(file_response.content)
            return local_path
        except Exception as ex:
            raise ValueError(f"Error al obtener un archivo random: {ex}")


    
    