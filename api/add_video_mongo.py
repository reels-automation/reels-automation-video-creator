import requests
import json

def add_video_mongo(url: str, data: dict):
    headers = {'Content-Type': 'application/json'} 
    print("posting to url : ", url)
    print("Data to post: ", data)
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response

