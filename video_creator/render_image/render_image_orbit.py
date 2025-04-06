import math
import numpy as np
from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *
from PIL import Image

class RenderImageOrbit(RenderImageStrategy):
    """Renders an images that makes an orbit around the center of the video

    Args:
        RenderImageStrategy: 
    """

    def render_image_animation(self, image: CustomImage, video_size: tuple[int, int]) -> ImageClip:
        
        pil_image = Image.open(image.image_path).convert("RGBA")
        movie_py_image = ImageClip(np.array(pil_image))

        resize_factor = 1/2 * image.resize_factor

        movie_py_image = movie_py_image.resized(height=resize_factor)
        
        center_x = video_size[0] / 2 - movie_py_image.size[0] / 2
        center_y = video_size[1] / 2 - movie_py_image.size[1] / 2
        radius = 40

        def circular_motion(t):
            return center_x + radius * np.cos((t/image.duration)*4 * math.pi) , 1/3 * video_size[1] + center_y + radius * np.sin((t / image.duration) *4 * math.pi)

        movie_py_image = (
            movie_py_image.with_duration(image.duration)
            .with_start(image.start_time)
            .with_position(circular_motion)
        )
      
        return movie_py_image