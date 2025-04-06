import math
import numpy as np
from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *
from PIL import Image

class RenderImageShake(RenderImageStrategy):
    """Renders an images that makes an orbit around the center of the video

    Args:
        RenderImageStrategy: 
    """

    def render_image_animation(self, image: CustomImage, video_size: tuple[int, int]) -> ImageClip:
        
        pil_image = Image.open(image.image_path).convert("RGBA")
        movie_py_image = ImageClip(np.array(pil_image))
        movie_py_image = movie_py_image.resized(height=image.resize_factor)
        
        center_x = video_size[0] / 2 - movie_py_image.size[0] / 2
        center_y = video_size[1] * 1/3 + video_size[1] / 2 - movie_py_image.size[1] / 2

        def shake(t):
            shake_strength_x = 30  
            shake_speed_x = 100

            shake_strength_y = 5  
            shake_speed_y = 30


            shake_x = shake_strength_x * np.sin(t * shake_speed_x)  
            shake_y = shake_strength_y * np.cos(t * shake_speed_y)  

            new_center_x = center_x + shake_x
            new_center_y = center_y + shake_y

            return new_center_x, new_center_y

        movie_py_image = (
            movie_py_image.with_duration(image.duration)
            .with_start(image.start_time)
            .with_position(shake)
        )
      
        return movie_py_image