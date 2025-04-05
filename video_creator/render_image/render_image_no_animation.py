from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *

class RenderImageNoAnimation(RenderImageStrategy):

    def render_image_animation(self, image: CustomImage) -> ImageClip:
        movie_py_image = ImageClip(image.image_path).resized(height=image.resize_factor)

        mask = movie_py_image.to_mask()
        mask = mask.resized(movie_py_image.size)  
        
        movie_py_image = movie_py_image.with_mask(mask)
        
        movie_py_image = movie_py_image

        movie_py_image = movie_py_image.with_start(image.start_time).with_duration(image.duration)


        return movie_py_image
