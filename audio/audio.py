from file_getter.file_getter import FileGetter

class Audio:
    
    def __init__(self, audio_path: str, file_getter : FileGetter , personaje: str =None):
        self.audio_path = audio_path
        self.personaje = personaje
        self.file_getter = file_getter
        self.duration = 0 
    