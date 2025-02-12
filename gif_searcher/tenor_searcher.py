import requests
import os
import json
from dotenv import load_dotenv

from gif_searcher.i_searcher import ISearcher

load_dotenv()
API_KEY = os.getenv("TENOR_API_KEY")


class TenorSearcher(ISearcher):
    
    def search_gif(self, phrase):
        lmt = 1
        ckey = "reels-automation"  # set the client_key for the integration and use the same value for all API calls
        
        response = requests.get(
            "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (phrase, API_KEY, ckey,  lmt))

        if response.status_code == 200:
            gif = json.loads(response.content)
            if gif and "results" in gif and len(gif["results"]) > 0:
                return gif["results"][0]["media_formats"]["gif"]["url"]
        
        return None 

