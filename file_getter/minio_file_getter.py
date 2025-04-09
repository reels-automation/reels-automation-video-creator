import os
from minio import Minio
from minio.error import S3Error
from file_getter.file_getter import FileGetter


class MinioFileGetter(FileGetter):
    def __init__(self):
        self.temp_folder = "temp_storage_minio"
        self.minio_client = Minio(
        "localhost:9000",
        access_key="AKIAIOSFODNN7EXAMPLE",
        secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        secure=False
        )

    def list_objects(self, bucket_name:str):
        return self.minio_client.list_objects(bucket_name)

    def get_file(self, file_name: str , file_location: str) -> str:
        local_path = os.path.join(self.temp_folder, file_name)
        try:
            self.minio_client.fget_object(
                bucket_name=file_location,
                object_name = file_name,
                file_path= local_path # Path to save the video that we get
            )
            return local_path
        except S3Error as err:            
            print(f"Error occurred: {err}")

    def get_random_file(self, file_location):
        return super().get_random_file(file_location)

    def upload_file(self, bucket_name: str, destination_file_name:str,audio_path:str):
        self.minio_client.fput_object(
            bucket_name,
            destination_file_name,
            audio_path

        )
        #os.remove(audio_path)
    