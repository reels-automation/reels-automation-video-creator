from PIL import Image
from image.image import CustomImage

class ImageHandler:

    def create_custom_image(self, image_name:str, start_time: int, duration:int,video_size:tuple[int,int]) -> CustomImage:
        """Creates a custom image

        Args:
            image_name (str): The name of the image
            start_time (int): Start time of the image in the video timeline
            duration (int): Duration of the image in the video timeline
            video_size (tuple[int,int]): Size of the background video 

        Returns:
            CustomImage: 
        """
        image_pillow = Image.open(image_name)
        image_width, image_height = image_pillow.size
        image_resize_factor = 1/3 * video_size[1]
        custom_image = CustomImage(image_name, image_width, image_height, start_time, duration, image_resize_factor)
        return custom_image


        




