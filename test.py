import os
import requests
import uuid
from file_getter.web_file_getter import WebImageFileGetter

getter = WebImageFileGetter()
name  = getter.get_file("Homero Simpson", "Homero Simpson")
print(name)