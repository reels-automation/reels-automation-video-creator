import random
from subtitles.subtitle_builder import SubtitleBuilder

class SubtitleDirector:
    
    @staticmethod
    def build_normal_subtitle(text:str, size:int):
        tema_builder = SubtitleBuilder(text, size)
        return tema_builder.build()

    @staticmethod
    def build_highlight_subtitle(text:str, size:int):
        tema_builder = SubtitleBuilder(text, size)
        tema_builder.add_color("yellow")
        tema_builder.increase_font_size(50)
        return tema_builder.build()

    @staticmethod
    def build_random_subtitle(text:str, size:int, percentage_of_highlight:int):
        """Builds a random subtitle
        Args:
            text (str): Text of the subtitle
            size (int): Size of the video 
            percentage_of_highlight (int): probability of the random text being a highlight text
        """

        true_percentage = 100-percentage_of_highlight
        random_number = random.randint(0,100)

        if random_number >= true_percentage:
            return SubtitleDirector.build_highlight_subtitle(text,size)
        
        return SubtitleDirector.build_normal_subtitle(text,size)

