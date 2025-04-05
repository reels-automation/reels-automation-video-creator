from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *
from PIL import Image
import numpy as np

class RenderImageNoAnimation(RenderImageStrategy):

    def render_image_animation(self, image: CustomImage) -> ImageClip:
        pil_image = Image.open(image.image_path).convert("RGB")  # Elimina canal alpha
        
        movie_py_image = ImageClip(np.array(pil_image))
        
        movie_py_image = movie_py_image.resized(height=image.resize_factor)
        movie_py_image = (
            movie_py_image.with_duration(image.duration)
            .with_start(image.start_time)
        )
        
        return movie_py_image
