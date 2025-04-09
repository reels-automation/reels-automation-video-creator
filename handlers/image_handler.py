from PIL import Image
from image.image import CustomImage
from file_getter.file_getter import FileGetter

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

    def create_random_images(self, number_of_images:int, file_getter: FileGetter, file_location:str, audio_duration:int, video_size:tuple[int,int])-> list[CustomImage]:
        """Creates a list of random images

        Args:
            number_of_images (int): Amount of images that will be rendered
            file_getter (FileGetter): FileGetter strategy to select the images
            file_location (str): Location where the file is saved, bucket-name, folder-name, etc
            audio_duration (int): Duration of the backgrund audio to divide the image length.
            video_size (tuple[int,int]): Size of the background video to resize each image.

        Returns:
            list[CustomImage]: Returns a list with instances of CustomImage.
        """
        custom_images_list = []
        start_time = 0
        image_duration = (audio_duration / number_of_images)
        
        for _ in range(number_of_images):            
            image_path = file_getter.get_random_file(file_location)
            custom_image = self.create_custom_image(image_path,start_time,audio_duration,video_size)
            start_time += image_duration
            custom_images_list.append(custom_image)
        
        return custom_images_list





            
            




        




