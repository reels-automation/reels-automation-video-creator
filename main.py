from quixstreams import Application
from PIL import Image
import os
import json
import random
import logging
import requests
import ast
import re

from audio.audio import Audio
from subtitles.subtitle_director import SubtitleDirector
from image.image import CustomImage
from file_getter.minio_file_getter import MinioFileGetter
from file_getter.file_getter_local_folder import FileGetterLocalFolder
from file_getter.web_file_getter import WebImageFileGetter
from video.video_director import VideoDirector
from video_creator.moviepy_video_creator import MoviePyVideoCreator
from kafka.consumer import create_consumer
from keyword_extractor.yake_extractor import extract_keywords, find_keyword_in_json
from gif_searcher.tenor_searcher import TenorSearcher
from gif_searcher.giphy_searcher import GiphySearcher
from utils.utils import get_keywords, clean_filename

from settings import ROOT_DIR, KAFKA_BROKER
from message.message import MessageBuilder

from video_creator.render_image.render_image_factory import RenderImageFactory

from handlers.audio_handler import AudioHandler
from handlers.image_handler import ImageHandler

# Set up logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    file_getter_local_folder = FileGetterLocalFolder()
    file_getter_web = WebImageFileGetter()
    video_creator = MoviePyVideoCreator()
    audio_handler = AudioHandler()
    image_handler = ImageHandler()
    
    print("enter here")

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
                            .add_instagram_account(response["instagram_account"])
                            .build()
                        )

        video_name = message.subtitles_name.split(".json")[0]
        
        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------
        #Get Gameplay
        temp_gameplay_folder = "temp_gameplay"
        gameplay_bucket_name = "gameplays"
        
        list_of_videos = ["60seconds1.mp4", "60seconds2.mp4","60valorant.mp4",
                          "clash-vertical1.mp4", "clash-vertical2.mp4", "Cuphead324x574.mp4", "dbd.mp4",
                            "flappy-ai.mp4", "fortnite-goga.mp4", "gettingoverit.mp4", "gta.mp4", "subway.mp4","subway2.mp4","subway3.mp4", "undertale1.mp4","undertale2.mp4"]
        
        if message.gameplay_name is None or message.gameplay_name == "":
            gameplay_object_name = random.choice(list_of_videos)
        else:
            gameplay_object_name = message.gameplay_name
        print("gameplay object name: ", gameplay_object_name)
        gameplay_file_location = minio_file_getter.get_file(gameplay_object_name, gameplay_bucket_name)
        name = gameplay_object_name.split(".")
        gameplay = video_director.build_gameplay(gameplay_file_location, name[0])
        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------
        
        #Get Audio.
        audio = audio_handler.get_audio(
            audio_bucket_name=message.tts_audio_bucket,
            audio_object_name=message.tts_audio_name,
            file_getter=minio_file_getter,
            temp_audio_folder="temp_audios"
            )                
        rendered_audio = video_creator.render_audio(audio)
        audio.duration = rendered_audio.duration

        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------
        #Get Image
        if message.pth_voice == "":
            message.pth_voice = "HOMERO SIMPSON LATINO"
        
        image_directory = f"temp_images/{message.pth_voice}"

        images_from_dir = os.listdir(image_directory)

        print("image dir :", images_from_dir)
        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------

        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------
        amount_of_images = 6
        render_image_factory = RenderImageFactory()
        rendered_video = video_creator.render_video(gameplay, audio.duration)
        
        clips = []
        audios = []
        audios.append(rendered_audio)
        clips.append(rendered_video)
        
        character_images = image_handler.create_random_images(amount_of_images, 
                                                              file_getter_web,
                                                              image_directory,
                                                              audio.duration,
                                                              rendered_video.size
                                                              )
        
        for custom_image in character_images:
            rendered_image = render_image_factory.render_image(render_image_factory.RANDOM, custom_image,rendered_video.size)
            clips.append(rendered_image)

        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------
        #Get and Render Subtitles
        temp_subtitles_folder = "temp_subtitles"
        subtitle_object_name = f"{video_name}.json"
        subtitles_bucket_name = "subtitles-json"
        subtitle_file_location = minio_file_getter.get_file(subtitle_object_name,subtitles_bucket_name)
        
        with open(subtitle_file_location, "r") as openfile:
            data = json.load(openfile)
        
        video_width = rendered_video.size[0]
        video_heigth = rendered_video.size[1]
        get_subtitles(data, video_width, video_heigth, video_creator, clips)
        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------
        

        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------
        video_creator.render_final_clip(video_name, clips, audios)
        
        bucket_name = "videos-homero"
        video_path = os.path.join(ROOT_DIR, "temp_vids",f"{video_name}.mp4")

        #print("XD: ", os.path.join(video_creator.temp_video_folder, video_name))

        minio_file_getter.upload_file(bucket_name, video_name,video_path)

        url = "http://localhost:5000/add-video"
        data = {"name": video_name, "bucket": bucket_name, "uploaded_to_cloudify":False,"uploaded_to_instagram": False, "instagram_account":message.instagram_account}
        headers = {'Content-Type': 'application/json'} 
        
        response = requests.post(url, data=json.dumps(data), headers= headers)
        #print("Status Code:", response.status_code)
        #print("Resposne, ", response.json())
        #--------------------------------------------[OTRA FUNCION]-------------------------------------------------

if __name__ == "__main__":
    main()
