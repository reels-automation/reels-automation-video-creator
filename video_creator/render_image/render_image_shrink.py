import math
import numpy as np
from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *
from PIL import Image

class RenderImageShrink(RenderImageStrategy):
    """Renders an images that makes an orbit around the center of the video

    Args:
        RenderImageStrategy: 
    """

    def render_image_animation(self, image: CustomImage, video_size: tuple[int, int]) -> ImageClip:
        
        pil_image = Image.open(image.image_path).convert("RGBA")
        movie_py_image = ImageClip(np.array(pil_image))
        movie_py_image = movie_py_image.resized(height=image.resize_factor)
        
        def shrink_size(t):
            resize_factor = 1 / (t+1)
            return resize_factor
        
        def adjust_center(t):
            center_x = video_size[0] / 2 - movie_py_image.size[0] / 2
            center_y = 1/3 * video_size[1] + (video_size[1] / 2 - movie_py_image.size[1] / 2)
            return center_x, center_y
            
        movie_py_image = (
            movie_py_image.with_duration(image.duration)
            .with_start(image.start_time)
            .resized(lambda t: shrink_size(t))
            .with_position(adjust_center)
        )
      
        return movie_py_image