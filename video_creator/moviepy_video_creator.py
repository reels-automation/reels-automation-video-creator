import math
from moviepy import *
from video.video import Video
from audio.audio import Audio
from image.image import CustomImage
from subtitles.subtitle import Subtitle
from video_creator.i_video_creator import IVideoCreator
from video_creator.render_image.render_image_factory import RenderImageFactory 


class MoviePyVideoCreator(IVideoCreator):

    def __init__(self, threads:int =8, fps:int = 24):
        self.temp_video_folder = "./temp_vids"
        self.threads = threads
        self.fps = fps

    def render_video(self, video: Video, duration: int) -> VideoFileClip:

        movie_py_video = VideoFileClip(video.video_path)
        movie_py_video = movie_py_video.with_duration(duration)
        return movie_py_video
       # movie_py_video.write_videofile(f'{self.temp_video_folder}/{video.name}.mp4',  threads = self.threads , fps = self.fps)
    
    def render_gif(self, video:Video, start_time:float, end_time:float, video_height:int):
        movie_py_gif = VideoFileClip(video.video_path)
        duration = end_time - start_time
        movie_py_gif = movie_py_gif.with_duration(duration).with_start(start_time)
        gif_offset = int(video_height * 0.3)  
        movie_py_gif = movie_py_gif.with_position(("center", (video_height // 2) - gif_offset))
        return movie_py_gif


    def render_audio(self, audio:Audio):
        movie_py_audio = AudioFileClip(audio.audio_path)
        return movie_py_audio
    
    def render_subtitle(self, subtitle:Subtitle, start_time: float, end_time:float, video_height:int):
        
        movie_py_subtitle = TextClip(
            font = subtitle.font,
            text = subtitle.text,
            font_size = subtitle.font_size,
            color = subtitle.color,
            stroke_color = subtitle.stroke_color,
            stroke_width = subtitle.stroke_width,
            text_align = subtitle.text_align,
            method = subtitle.method,
            size = subtitle.size,
            margin = subtitle.margin
        )
        
        duration = end_time - start_time
        movie_py_subtitle = movie_py_subtitle.with_duration(duration).with_start(start_time)
        movie_py_subtitle = movie_py_subtitle.with_position(("center", video_height // 2))
        
        return movie_py_subtitle
    
    def render_image(self, image:CustomImage, animation_pattern:str):
        return RenderImageFactory().render_image(animation_pattern, image)
    
    def render_final_clip(self, name:str, list_of_clips: list, list_of_audio_clip: list[AudioFileClip] = None):
        final_clip = CompositeVideoClip(list_of_clips)
        final_audio = CompositeAudioClip(list_of_audio_clip)
        
        if len(list_of_audio_clip) > 0 :
            final_clip.audio = final_audio

        file_destination = f"{self.temp_video_folder}/{name}.mp4"

        final_clip.write_videofile(file_destination, threads=self.threads, fps=self.fps)


    
