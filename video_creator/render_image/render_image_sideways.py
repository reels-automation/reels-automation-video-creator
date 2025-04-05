from video_creator.render_image.render_image_strategy import RenderImageStrategy
from image.image import CustomImage
from moviepy import *
from PIL import Image
import numpy as np

class RenderImageSideways(RenderImageStrategy):

    def render_image_animation(self, image: CustomImage, video_size: tuple[int, int]) -> ImageClip:
        pil_image = Image.open(image.image_path).convert("RGB")
        movie_py_image = ImageClip(np.array(pil_image))
        
        movie_py_image = movie_py_image.resized(height=image.resize_factor)
        
        direction_modifier = -1

        def get_position(t):
            try:
                nonlocal direction_modifier
                speed_factor = 70  # Factor de velocidad para ajustar cuánto se mueve por cada incremento de t
                
                # Inicializamos x en el centro de la pantalla
                x = video_size[0] // 2  # Centro horizontal de la pantalla

                # Movemos la imagen dependiendo del valor de t (positivo o negativo)
                x += direction_modifier * t * speed_factor
                
                # Comprobamos si la imagen ha alcanzado los bordes de la pantalla y hacemos que rebote
                if x >= video_size[0] -  200:  # Límite derecho (con un pequeño margen)
                    direction_modifier = -1  # Invertir dirección para mover hacia la izquierda
                    x = video_size[0] -  50  # Ajustar para que no sobrepase el borde

                elif x <= 50:  # Límite izquierdo (con un pequeño margen)
                    direction_modifier = 1  # Invertir dirección para mover hacia la derecha
                    x = 50  # Ajustar para que no sobrepase el borde

                # Mantener la posición de y en la parte inferior de la pantalla
                y = video_size[1] - movie_py_image.h - 50

                # Imprimimos el valor de x para ver cómo se mueve
                print("X value: ", x)

                return (x, y)
            
            except Exception as e:
                print("Exception: ", e)
                return (0, 0)


        
        # 4. Configurar animación
        movie_py_image = (
            movie_py_image.with_duration(image.duration)
            .with_start(image.start_time)
            .with_position(get_position)
        )
      
        return movie_py_image