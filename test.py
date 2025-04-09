import os
import requests
import uuid
from file_getter.web_file_getter import WebImageFileGetter

getter = WebImageFileGetter(temp_folder="temp_images")
img_path = getter.get_file("gatito.jpg", "https://picsum.photos/400/300")
print(f"Imagen guardada en: {img_path}")

random_img = getter.get_random_file("https://picsum.photos/400/300")
print(f"Imagen aleatoria guardada en: {random_img}")