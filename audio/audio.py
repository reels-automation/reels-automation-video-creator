from file_getter.file_getter import FileGetter

class Audio:
    
    def __init__(self, audio_path: str, personaje: str =None):
        self.audio_path = audio_path
        self.personaje = personaje
        self.__duration = 0
    
    @property
    def duration(self):
        return self.__duration
    
    @duration.setter
    def duration(self, new_duration):
        self.__duration = new_duration
