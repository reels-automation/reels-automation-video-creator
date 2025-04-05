class CustomImage():
    def __init__(self, image_path:str, width:int, height: int, start_time:int, duration:int, resize_factor: int):
        self.image_path = image_path
        self.width = width
        self.height = height
        self.start_time = start_time
        self.duration = duration
        self.resize_factor = resize_factor
