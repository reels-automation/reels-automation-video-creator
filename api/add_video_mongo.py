import requests
import json
import time
from settings import API_GATEWAY_URL


def add_video_mongo(url: str, data: dict, video_name: str):
    headers = {'Content-Type': 'application/json'}
    get_video_api_url = f"{API_GATEWAY_URL}get-video"
    payload = {"video_name": f"{video_name}.mp4"}

    max_retries = 3
    backoff_base = 5  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            print(f"GET_VIDEO URL attempt {attempt}: {get_video_api_url}")
            print("payload: ", payload)
            print("get_video_api_url; ", get_video_api_url)
            print("headers: ", headers)
            response_video = requests.post(get_video_api_url, json=payload, headers=headers, timeout=10)
            print("response_video: ", response_video)
            response_video.raise_for_status()
            video_data = response_video.json()
            # Retry if response is empty or missing 'url'
            if not video_data or 'url' not in video_data or not video_data['url']:
                raise ValueError("Empty or invalid response")
            print("Video data received:", video_data)
            break  # Success
        except (requests.RequestException, ValueError) as e:
            print(f"[Attempt {attempt}] Error fetching video URL: {e}")
            if attempt == max_retries:
                raise
            sleep_time = backoff_base ** attempt
            print(f"Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)

    # Merge and send to MongoDB
    data.update(video_data)
    print("Posting to Mongo URL:", url)
    print("Data:", data)

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response
