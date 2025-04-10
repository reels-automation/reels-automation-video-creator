import os
import requests
import random
import uuid
import base64
from file_getter.file_getter import FileGetter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class WebImageFileGetter(FileGetter):
    def __init__(self):
        self.temp_folder = "temp_storage_web"
        os.makedirs(self.temp_folder, exist_ok=True)

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        chrome_driver_path = "/usr/bin/chromedriver"
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Definir resolución mínima
        self.min_width = 150
        self.min_height = 150
    
    def _add_noise_to_search_term(self, term):
        suffixes = ["", " art", " 4k", " hd", " funny", " cartoon", " meme"]
        return term + random.choice(suffixes)

    def _search_and_download(self, search_term: str, file_name: str = None) -> str:
        
        search_term = self._add_noise_to_search_term(search_term)
        query = f"https://www.google.com/search?q={search_term}&tbm=isch"
        self.driver.get(query)

        images = self.driver.find_elements(By.CLASS_NAME, 'YQ4gaf')
        random.shuffle(images)
        for index, image in enumerate(images):
            try:
                image_data = image.get_attribute('src')
                width = image.get_attribute('width')
                height = image.get_attribute('height')

                if width is None or height is None:
                    continue

                width = int(width)
                height = int(height)

                if width >= self.min_width and height >= self.min_height:
                    if image_data and image_data.startswith('data:image/jpeg;base64,'):
                        base64_image = image_data.split('base64,')[1]
                        img_data = base64.b64decode(base64_image)

                        # Asignar nombre
                        final_file_name = file_name if file_name else f"{uuid.uuid4().hex}.jpg"
                        local_path = os.path.join(self.temp_folder, f"{final_file_name}.png")

                        with open(local_path, 'wb') as f:
                            f.write(img_data)

                        return local_path
            except Exception as e:
                print(f"Error al procesar imagen {index}: {e}")
        raise Exception("No se pudo encontrar una imagen válida.")

    def get_file(self, file_name: str, file_location: str) -> str:
        """
        file_name: nombre con el que se guardará la imagen localmente
        file_location: string a usar como término de búsqueda
        """
        return self._search_and_download(file_location, file_name)

    def get_random_file(self, file_location: str) -> str:
        return self._search_and_download(file_location)

    def upload_file(self):
        pass  # No implementado aún

