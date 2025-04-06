import os
from minio import Minio
from minio.error import S3Error
from file_getter.file_getter import FileGetter


class MinioFileGetter(FileGetter):
    def __init__(self):
        
        self.minio_client = Minio(
        "localhost:9000",
        access_key="AKIAIOSFODNN7EXAMPLE",
        secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        secure=False
        )

    def list_objects(self, bucket_name:str):
        return self.minio_client.list_objects(bucket_name)

    def get_file_temp_folder(self, temp_folder:str,  object_name: str , bucket_name: str) -> str:
        local_path = os.path.join(temp_folder, object_name)
        try:
            self.minio_client.fget_object(
                bucket_name=bucket_name,
                object_name = object_name,
                file_path= local_path # Path to save the video that we get
            )
            return local_path
        except S3Error as err:            
            print(f"Error occurred: {err}")

    def upload_file(self, bucket_name: str, destination_file_name:str,audio_path:str):
        self.minio_client.fput_object(
            bucket_name,
            destination_file_name,
            audio_path

        )
        #os.remove(audio_path)
    