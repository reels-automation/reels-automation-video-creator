class Subtitle:
    def __init__(self, text:str, font: str, font_size:int, color:str, stroke_color:str, stroke_width:int, text_align:str, method:str, size:int, margin:tuple[int]):
        self.text = text
        self.font = font
        self.font_size = font_size
        self.color = color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.text_align = text_align
        self.method = method
        self.size = size
        self.margin = margin
