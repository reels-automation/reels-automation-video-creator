
from video.video import Video
from audio.audio import Audio
from subtitles.subtitle import Subtitle

from abc import ABC

class IVideoCreator(ABC):
    def __init__(self):
        pass
    
    def render_video(self, video: Video):
        """Renders a video

        Args:
            video (Video): 
        """

    def render_audio(self, audio: Audio):
        """Renders an audio

        Args:
            audio (Audio): 
        """
    
    def render_subtitle(self, subtitle: Subtitle):
        """Renders a subtitle

        Args:
            subtitle (Subtitle): 
        """

    def render_image(self, image: "Image"):
        """Renders an image

        Args:
            image (Image): 
        """

    def render_final_clip(self):
        """Renders final clip 
        """

