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

    