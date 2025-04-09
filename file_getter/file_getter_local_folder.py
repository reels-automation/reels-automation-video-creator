import os
import random
from file_getter.file_getter import FileGetter

class FileGetterLocalFolder(FileGetter):

    def get_file(self, file_name:str, file_location:str)->str:
        image_path = os.path.join(file_location, f"{file_name}")
        return image_path
    
    def get_random_file(self, file_location):
        
        image_names_from_folder = os.listdir(file_location)
        random_image_name_from_dir = random.choice(image_names_from_folder)
        image_path = os.path.join(file_location, random_image_name_from_dir)
        return image_path


        
