from quixstreams import Application
import os
import json
import random
import logging
import requests
import ast
import re

from audio.audio import Audio
from subtitles.subtitle_director import SubtitleDirector
from image.image import Image
from file_getter.minio_file_getter import MinioFileGetter
from video.video_director import VideoDirector
from video_creator.moviepy_video_creator import MoviePyVideoCreator
from kafka.consumer import create_consumer
from keyword_extractor.yake_extractor import extract_keywords, find_keyword_in_json
from gif_searcher.tenor_searcher import TenorSearcher
from gif_searcher.giphy_searcher import GiphySearcher
from utils.utils import get_keywords, clean_filename

from settings import ROOT_DIR, KAFKA_BROKER
from message.message import MessageBuilder

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_subtitles(subtitles_json:dict, video_width:int, video_height:int, video_creator:MoviePyVideoCreator, clips:list):
    """Gets the subtitles from a json file

    Args:
        subtitles_json (dict): The json where the subtitles are located
        video_width (int): The width of the background video
        video_height (int): The height of the background video
        video_creator (MoviePyVideoCreator): Instance of the video creator class
        clips (list): List of clips to append the rendered subtitles
    """
    for subtitle in subtitles_json:        
            word = subtitle["word"].upper()
            start_time = subtitle["start"]
            end_time = subtitle["end"]
            subtitle_director = SubtitleDirector()
            highligthed_word_percentage = 0
            sub = subtitle_director.build_random_subtitle(word,video_width,highligthed_word_percentage)
            rendered_subtitle = video_creator.render_subtitle(sub, start_time, end_time, video_height)
            clips.append(rendered_subtitle)

def main():
    
    video_director = VideoDirector()
    minio_file_getter = MinioFileGetter()
    video_creator = MoviePyVideoCreator()
    HAS_GIFS = False

    while True:
        consumer = Application(broker_address=KAFKA_BROKER, loglevel="DEBUG")
        topic_to_subscribe = "subtitles-audios"
        response = create_consumer(consumer, topic_to_subscribe)

        print("response: ", response)

        message_builder = MessageBuilder(response["tema"])
        message = (message_builder
                            .add_personaje(response["personaje"])
                            .add_script(response["script"])
                            .add_tts_audio_name(response["tts_audio_name"])
                            .add_tts_audio_bucket(response["tts_audio_bucket"])
                            .add_subtitles_name(response["subtitles_name"])
                            .add_subtitles_bucket(response["subtitles_bucket"])
                            .add_author(response["author"])
                            .add_pitch(response["pitch"])
                            .add_tts_voice(response["tts_voice"])
                            .add_tts_rate(response["tts_rate"])
                            .add_pth_voice(response["pth_voice"])
                            .add_gameplay_name(response["gameplay_name"])
                            .build()
                        )

        video_name = message.subtitles_name.split(".json")[0]
        
        #Get Gameplay
        temp_gameplay_folder = "temp_gameplay"
        gameplay_bucket_name = "gameplays"
        
        list_of_videos = ["60seconds1.mp4", "60seconds2.mp4","60valorant.mp4",
                          "clash-vertical1.mp4", "clash-vertical2.mp4", "Cuphead324x574.mp4", "dbd.mp4",
                            "flappy-ai.mp4", "fortnite-goga.mp4", "gettingoverit.mp4", "gta.mp4", "subway.mp4","subway2.mp4","subway3.mp4"]
        
        if message.gameplay_name is None or message.gameplay_name == "":
            gameplay_object_name = random.choice(list_of_videos)
        else:
            gameplay_object_name = message.gameplay_name

        
        print("gameplay object name: ", gameplay_object_name)
        gameplay_file_location = minio_file_getter.get_file_temp_folder(temp_gameplay_folder, gameplay_object_name, gameplay_bucket_name)

        name = gameplay_object_name.split(".")
        gameplay = video_director.build_gameplay(gameplay_file_location, name[0])
        
        #Get audio
        temp_audio_folder = "temp_audios"
        audio_bucket_name = message.tts_audio_bucket
        audio_object_name = message.tts_audio_name

        audio_file_location = minio_file_getter.get_file_temp_folder(temp_audio_folder,audio_object_name,audio_bucket_name)
        
        audio = Audio(audio_file_location, None, message.personaje)
        rendered_audio = video_creator.render_audio(audio)
        audio_duration = rendered_audio.duration

        image_directory = f"temp_images/{message.pth_voice}"
        images_from_dir = os.listdir(image_directory)

        print("image dir :", images_from_dir)

        image_name = os.path.join(image_directory, f"{random.choice(images_from_dir)}")


        print("image name: ", image_name)

        
        
        image = Image(image_name)

        rendered_video = video_creator.render_video(gameplay, audio_duration)
        resize_factor = 1/3 * rendered_video.size[1]
        rendered_homer_image = video_creator.render_image(image, resize_factor, audio_duration)
        
        clips = []
        audios = []
        audios.append(rendered_audio)
        clips.append(rendered_video)
        clips.append(rendered_homer_image)

        #Get and Render Subtitles
        temp_subtitles_folder = "temp_subtitles"
        subtitle_object_name = f"{video_name}.json"
        subtitles_bucket_name = "subtitles-json"
        subtitle_file_location = minio_file_getter.get_file_temp_folder(temp_subtitles_folder,subtitle_object_name,subtitles_bucket_name)
        
        with open(subtitle_file_location, "r") as openfile:
            data = json.load(openfile)
        
        script = ""
        video_width = rendered_video.size[0]
        video_heigth = rendered_video.size[1]
        get_subtitles(data, video_width, video_heigth, video_creator, clips)


        if HAS_GIFS:

            keywords = extract_keywords(script)
            gif_searcher = TenorSearcher()

            new_keywords = str([word[0] for word in keywords])


            better_keywords = get_keywords(new_keywords)

            list_keywords = []

            current_word = ""
            

            for char in better_keywords:
                print("Char , ", char)
                
                if char != "[" and char != "," and char != "]":
                    current_word += char
                else:
                    cleaned_word = clean_filename(current_word)
                    list_keywords.append(cleaned_word)
                    current_word = ""

                    
            gif_start_time = 0
            for index , keyword in enumerate(list_keywords):
                
                gif_url = gif_searcher.search_gif(keyword)
                if gif_url:

                    gif_location = f"temp_gifs/{keyword}.gif"
                    gif_searcher.download_gif(gif_url, gif_location)
                    gif_video = video_director.build_gif(gif_location, keyword)
                    gif_end_time = gif_start_time + 3
                    gifclip = video_creator.render_gif(gif_video, gif_start_time, gif_end_time, rendered_video.size[1])
                    clips.append(gifclip)
                    gif_start_time = gif_end_time + 6

                else:
                    print(f"No gif found for: {keyword}")
        
        video_creator.render_final_clip(video_name, clips, audios)
        
        bucket_name = "videos-homero"
        video_path = os.path.join(ROOT_DIR, "temp_vids",f"{video_name}.mp4")

        print("XD: ", os.path.join(video_creator.temp_video_folder, video_name))

        minio_file_getter.upload_file(bucket_name, video_name,video_path)

        url = "http://localhost:5000/add-video"
        data = {"name": video_name, "bucket": bucket_name, "uploaded_to_cloudify":False,"uploaded_to_instagram": False}
        headers = {'Content-Type': 'application/json'} 
        
        response = requests.post(url, data=json.dumps(data), headers= headers)
        print("Status Code:", response.status_code)
        print("Resposne, ", response.json())



if __name__ == "__main__":
    main()
