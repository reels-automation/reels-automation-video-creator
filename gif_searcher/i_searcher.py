from abc import ABC
import requests

class ISearcher(ABC):
    def search_gif(self, phrase:str) -> str | None:
        """Searchs for a gif given a phrase

        Args:
            phrase (str): phrase to search a gif

        Returns:
            str | None: Return a url or None if no gif is found
        """
    
    def download_gif(self, gif_url:str, filename:str):
        response = requests.get(gif_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")

    
