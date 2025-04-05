from abc import ABC
from image.image import CustomImage

class RenderImageStrategy(ABC):

    def render_image_animation(self, image:CustomImage):
        """Renders an image with a specific animation
        Args:
            image (CustomImage): 
        """
        pass
        
