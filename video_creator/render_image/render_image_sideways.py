from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *
from PIL import Image
import numpy as np

class RenderImageSideways(RenderImageStrategy):

    def render_image_animation(self, image: CustomImage) -> ImageClip:

        # Abrir imagen con PIL y remover transparencia
        pil_image = Image.open(image.image_path).convert("RGB")  # Elimina canal alpha
        
        # Crear ImageClip desde el array de numpy
        movie_py_image = ImageClip(np.array(pil_image))
        
        # Redimensionar
        movie_py_image = movie_py_image.resized(height=image.resize_factor)
        
        # Configurar animación
        movie_py_image = (
            movie_py_image.with_duration(image.duration)
            .with_start(image.start_time)
            .with_position(lambda t: (50 + t * (movie_py_image.w + 50) / image.duration, 50))
        )
        
        return movie_py_image