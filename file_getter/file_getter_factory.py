import random
from file_getter.file_getter import FileGetter
from file_getter.file_getter_local_folder import FileGetterLocalFolder
from file_getter.minio_file_getter import MinioFileGetter
from file_getter.web_file_getter import WebImageFileGetter





class FileGetterFactory:
    """Factory of the file getter strategy
    """

    LOCAL_FOLDER = "LOCAL_FOLDER"
    minio = "MINIO"
    WEBIMAGE = "WEBIMAGE"
    RANDOM = "RANDOM"

    ALL_GETTERS = [LOCAL_FOLDER,WEBIMAGE]

    @staticmethod
    def create_file_getter(file_getter_name:str) -> FileGetter:
        if file_getter_name == FileGetterFactory.LOCAL_FOLDER:
            return FileGetterLocalFolder()
        elif file_getter_name == FileGetterFactory.minio:
            return MinioFileGetter()
        elif file_getter_name == FileGetterFactory.WEBIMAGE:
            return WebImageFileGetter()
        elif file_getter_name == FileGetterFactory.RANDOM:
            return FileGetterFactory.create_file_getter(random.choice(FileGetterFactory.ALL_GETTERS))