from quixstreams import Application
import os
import json
import random
import logging
import ast

from audio.audio import Audio
from subtitles.subtitle import Subtitle
from image.image import Image
from file_getter.minio_file_getter import MinioFileGetter
from video.video_director import VideoDirector
from video_creator.moviepy_video_creator import MoviePyVideoCreator
from kafka.consumer import create_consumer
from keyword_extractor.yake_extractor import extract_keywords, find_keyword_in_json

from gif_searcher.tenor_searcher import TenorSearcher
from gif_searcher.giphy_searcher import GiphySearcher
from utils.utils import get_keywords

from settings import ROOT_DIR

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    
    video_director = VideoDirector()
    minio_file_getter = MinioFileGetter()
    video_creator = MoviePyVideoCreator()

    while True:
        consumer = Application(broker_address="localhost:9092", loglevel="DEBUG")
        topic_to_subscribe = "subtitles-audios"
        response = create_consumer(consumer, topic_to_subscribe)

        video_name = response["subtitles_name"].split(".json")[0]
        
        #Get Gameplay
        temp_gameplay_folder = "temp_gameplay"
        gameplay_bucket_name = "gameplays"
        
        list_of_videos = ["60seconds1.mp4", "60seconds2.mp4","60valorant.mp4", "beni-survivors.mp4",
                          "clash-vertical1.mp4", "clash-vertical2.mp4", "Cuphead324x574.mp4", "dbd.mp4",
                            "flappy-ai.mp4", "fortnite-goga.mp4", "gettingoverit.mp4", "gta.mp4", "subway.mp4","subway2.mp4","subway3.mp4"]


        gameplay_object_name = random.choice(list_of_videos)

        gameplay_file_location = minio_file_getter.get_file_temp_folder(temp_gameplay_folder, gameplay_object_name, gameplay_bucket_name)

        name = gameplay_object_name.split(".")
        gameplay = video_director.build_gameplay(gameplay_file_location, name[0])
        
        #Get audio
        temp_audio_folder = "temp_audios"
        audio_bucket_name = "audios-tts"
        audio_object_name = f"{video_name}.mp3"

        audio_file_location = minio_file_getter.get_file_temp_folder(temp_audio_folder,audio_object_name,audio_bucket_name)
        
        audio = Audio(audio_file_location, None, "Homero Simpson")
        rendered_audio = video_creator.render_audio(audio)
        audio_duration = rendered_audio.duration

        #Image
        image = Image("temp_images/homero.png")

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


        for subtitle in data:
            
            word = subtitle["word"]
            script += f" {word}"
            start_time = subtitle["start"]
            end_time = subtitle["end"]

            font = "resources/fonts/TikTokDisplay-Bold.ttf"
            font_size = 60
            word = word.upper()
            sub = Subtitle(word,font,font_size,"white","black",4,"center","caption", (rendered_video.size[0]-font_size,None), (20,10))
            
            rendered_subtitle = video_creator.render_subtitle(sub, start_time, end_time, rendered_video.size[1])
            clips.append(rendered_subtitle)

        keywords = extract_keywords(script)
        
        every_json_word = []
        gif_searcher = TenorSearcher()

        new_keywords = str([word[0] for word in keywords])


        better_keywords = get_keywords(new_keywords)

        better_keywords = ast.literal_eval(better_keywords)

        list_keywords = []

        current_word = ""
        for char in better_keywords:
            
            if char != "[" or char != "," or char != "]":
                current_word += char
            else:
                list_keywords.append(current_word)
                current_word = ""

        print(list_keywords)
        
        for keyword,score in keywords:
            gif_url = gif_searcher.search_gif(keyword)
            if gif_url:

                gif_location = f"temp_gifs/{keyword}.gif"
                gif_searcher.download_gif(gif_url, gif_location)
                #resize_gif(gif_url, rendered_video.size[0],rendered_video.size[1], gif_location)                
                json_word = find_keyword_in_json(data,keyword)
                
                every_json_word.append((json_word,gif_location))
                print("every json:", every_json_word)
                sorted_json = sorted(every_json_word, key=lambda x: x[0]['start'])
        
            else:
                print(f"No gif found for: {keyword}")
        
        for index, data in enumerate(sorted_json):

            current_word = data[0]
            

            if index +1 < len(sorted_json): 
                next_word = sorted_json[index+1][0]
            else:
                next_word = None 

            gif_video = video_director.build_gif(data[1], current_word["word"])
            
            gif_start_time = current_word["start"]
            
            if next_word is not None:
                gif_end_time = next_word["end"]
            else:
                gif_end_time = current_word["end"] +3

            if (gif_end_time - gif_start_time) > 3:
                gif_end_time = gif_start_time +3

            gifclip = video_creator.render_gif(gif_video, gif_start_time, gif_end_time, rendered_video.size[1])
            clips.append(gifclip)
        
        video_creator.render_final_clip(video_name, clips, audios)
        
        bucket_name = "videos-homero"
        video_path = os.path.join(ROOT_DIR, "temp_vids",f"{video_name}.mp4")

        print("XD: ", os.path.join(video_creator.temp_video_folder, video_name))

        minio_file_getter.upload_file(bucket_name, video_name,video_path)


if __name__ == "__main__":
    main()
