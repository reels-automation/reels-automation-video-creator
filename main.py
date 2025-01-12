from quixstreams import Application
import os
import json
import random
import logging
from audio.audio import Audio
from subtitles.subtitle import Subtitle
from image.image import Image
from file_getter.minio_file_getter import MinioFileGetter
from video.video_director import VideoDirector
from video_creator.moviepy_video_creator import MoviePyVideoCreator
from kafka.consumer import create_consumer
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
        audio_bucket_name = "audios-homero"
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
        
        for subtitle in data:
            
            word = subtitle["word"]
            start_time = subtitle["start"]
            end_time = subtitle["end"]

            font = "resources/fonts/p5hatty.ttf"
            font_size = 100
            sub = Subtitle(word,font,font_size,"white","black",4,"center","caption", (rendered_video.size[0]-font_size,None), (20,10))
            
            print("Caca", rendered_video.size[1])
            rendered_subtitle = video_creator.render_subtitle(sub, start_time, end_time, rendered_video.size[1])
            clips.append(rendered_subtitle)




        video_creator.render_final_clip(video_name, clips, audios)
        
        bucket_name = "videos-homero"
        video_path = os.path.join(ROOT_DIR, "temp_vids",f"{video_name}.mp4")

        print("XD: ", os.path.join(video_creator.temp_video_folder, video_name))

        minio_file_getter.upload_file(bucket_name, video_name,video_path)







if __name__ == "__main__":
    main()
