from video.video import Video
class VideoBuilder:

    def __init__(self, video_path: str , name:str):
        self.video = Video(video_path, name)
    
    def add_subtitle(self, subtitle):
        self.video.subtitles.append(subtitle)
    
    def add_audio(self, audio):
        self.video.audios.append(audio)
    
    def add_video(self, video: Video):
        self.video.videos.append(video)
    
    def build(self) -> Video:
        return self.video
    