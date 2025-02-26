class Subtitle:
    def __init__(self, text:str, size:int, font: str="resources/fonts/TikTokDisplay-Bold.ttf", font_size:int=60, color:str="white", stroke_color:str="black", stroke_width:int=4, text_align:str="center", method:str="caption", margin:tuple[int]=(20,10)):
        self.text = text
        self.size = (size-font_size,None)
        self.font = font
        self.font_size = font_size
        self.color = color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.text_align = text_align
        self.method = method
        self.margin = margin
