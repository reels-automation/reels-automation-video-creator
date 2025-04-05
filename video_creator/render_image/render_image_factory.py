import random
from video_creator.render_image.render_image_strategy import RenderImageStrategy
from video_creator.render_image.render_image_sideways import RenderImageSideways
from video_creator.render_image.render_image_no_animation import RenderImageNoAnimation
from image.image import CustomImage

class RenderImageFactory:
    """Factory of the strategy patterns that render images
    """

    NO_ANIMATION = "noanimation"
    SIDEWAYS = "sideways"
    RANDOM = "random"

    ALL_IMAGES = [NO_ANIMATION, SIDEWAYS]

    @staticmethod
    def render_image(render_image_strategy:str, image:CustomImage, video_size:tuple[int,int]):
        
        if render_image_strategy == RenderImageFactory.NO_ANIMATION:
            image_renderer = RenderImageNoAnimation()
            return image_renderer.render_image_animation(image,video_size)
        
        elif render_image_strategy == RenderImageFactory.SIDEWAYS:
            image_renderer = RenderImageSideways()
            return image_renderer.render_image_animation(image,video_size)

        elif render_image_strategy == RenderImageFactory.RANDOM:
            strategy = random.choice(RenderImageFactory.ALL_IMAGES)
            return RenderImageFactory.render_image(strategy, image, video_size)




