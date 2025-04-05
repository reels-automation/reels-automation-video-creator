from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *

class RenderImageSideways(RenderImageStrategy):

    def render_image_animation(self, image:CustomImage) -> ImageClip:
        """Renders an image that moves sideways

        Args:
            image (CustomImage): _description_

        Returns:
            ImageClip: _description_
        """
        movie_py_image = ImageClip(image.image_path).resized(height=image.resize_factor)

        # Crear una máscara para la imagen
        mask = movie_py_image.to_mask()
        mask = mask.resized(movie_py_image.size)  # Redimensionar la máscara para que coincida con el tamaño de la imagen
        
        movie_py_image = movie_py_image.with_mask(mask)
        
        movie_py_image = movie_py_image

        # Configurar la duración y el inicio
        movie_py_image = movie_py_image.with_start(image.start_time).with_duration(image.duration)

        # Mover la imagen de izquierda a derecha (sideways)
        # A medida que pasa el tiempo (t), la posición de la imagen cambia
        movie_py_image:ImageClip
        movie_py_image.to_RGB()
        #movie_py_image.with_background_color(color=(255,20,40))
        movie_py_image = movie_py_image.with_position(lambda t: (50 + t * (movie_py_image.size[0] + 50) / image.duration, 50))

        return movie_py_image