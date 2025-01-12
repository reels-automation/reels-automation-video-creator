from video.video_builder import VideoBuilder
from video.video import Video
from audio.audio import Audio
from subtitles.subtitle import Subtitle

class VideoDirector():
    
    @staticmethod
    def build_reel(video_path: str, name:str, gameplay: Video, audio: Audio, subtitle: Subtitle):
        video_builder = VideoBuilder(video_path, name)
        video_builder.add_subtitle(subtitle)
        video_builder.add_audio(audio)
        video_builder.add_video(gameplay)
        return video_builder.build()
    
    @staticmethod
    def build_gameplay(video_path:str, name:str):
        video_builder = VideoBuilder(video_path, name)
        return video_builder.build()
