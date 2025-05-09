import requests
import json
from settings import API_GATEWAY_URL


def add_video_mongo(url: str, data: dict, video_name: str):
    headers = {'Content-Type': 'application/json'}

    # Primer POST para obtener la URL del video
    get_video_api_url = f"{API_GATEWAY_URL}get-video"

    print("GET_VIDEO URL : ", get_video_api_url)

    payload = {"video_name": f"{video_name}.mp4"}
    response_video = requests.post(get_video_api_url, json=payload, headers=headers)
    response_video.raise_for_status()

    print("Response video: ", response_video)
    print("Response video: ", response_video.json())

    video_data = response_video.json()  # por ejemplo: {'url': 'http://...'}

    data.update(video_data)

    print("video_url:", video_data)
    print("posting to url:", url)
    print("Data to post:", data)

    # Segundo POST para guardar el video en Mongo
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response

