from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *
from PIL import Image
import numpy as np

class RenderImageNoAnimation(RenderImageStrategy):

    def render_image_animation(self, image: CustomImage,video_size:tuple[int,int]) -> ImageClip:
        pil_image = Image.open(image.image_path).convert("RGBA")
        movie_py_image = ImageClip(np.array(pil_image))
        movie_py_image = movie_py_image.resized(height=image.resize_factor)

        def adjust_center(t):
            center_x = (video_size[0] // 2) - (movie_py_image.w // 2)
            center_y = (video_size[1] // 3) - (movie_py_image.h // 2)
            return (center_x, center_y)


        movie_py_image = (
            movie_py_image.with_duration(image.duration)
            .with_start(image.start_time)
            .with_position(adjust_center)
        )
        
        return movie_py_image
