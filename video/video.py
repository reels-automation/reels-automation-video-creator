class Video:
    
    def __init__(self, video_path: str, name:str, duration:int=None, subtitles:list=[], audios: list = [] , videos:list = []):
        
        self.video_path = video_path
        self.name = name
        self.duration = duration
        self.subtitles = subtitles
        self.audios = audios
        self.videos = videos


    