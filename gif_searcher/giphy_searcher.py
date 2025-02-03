import requests
import os
from dotenv import load_dotenv

from gif_searcher.i_searcher import ISearcher

load_dotenv()
API_KEY = os.getenv("GIPHY_API_KEY")


class GiphySearcher(ISearcher):
    
    def search_gif(self, phrase):
        url = f"https://api.giphy.com/v1/gifs/search?q={phrase}&api_key={API_KEY}&limit=1"
        response = requests.get(url).json()
        
        if response['data']:
            gif_url = response['data'][0]['images']['downsized']['url']
            return gif_url
        return None

