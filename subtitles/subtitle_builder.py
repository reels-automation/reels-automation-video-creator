from subtitles.subtitle import Subtitle

class SubtitleBuilder:
    def __init__(self, text:str, size: int):
        self.subtitle = Subtitle(text, size)
    
    def add_font(self, font: str):
        self.subtitle.font = font

    def add_font_size(self, font_size:int):
        self.subtitle.font_size = font_size
    
    def increase_font_size(self, increase_percentage):
        self.subtitle.font_size *= (1+(increase_percentage/100))

    def add_color(self, color:str):
        self.subtitle.color = color

    def add_stroke_color(self, color: str):
        self.subtitle.stroke_color = color

    def add_stroke_width(self, stroke_width:int):
        self.subtitle.stroke_width = stroke_width
    
    def add_margin(self, margin:tuple[int]):
        self.subtitle.margin = margin

    def build(self) -> Subtitle:
        return self.subtitle


        