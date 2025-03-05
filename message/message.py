from dataclasses import dataclass
from utils.utils import sanitize_attribute

@dataclass
class Message:
    tema: str
    personaje: str = ""
    script: str = ""
    tts_audio_name: str = ""
    tts_audio_bucket: str = ""
    subtitles_name: str = ""
    subtitles_bucket: str = ""
    author: str = ""
    pitch: int = 0 
    tts_voice: str = ""
    tts_rate: int = 0
    pth_voice: str = ""
    gameplay_name: str = ""
    instagram_account: str = ""

    def to_dict(self):
        return self.__dict__

class MessageBuilder:
    def __init__(self, tema: str):
        self.message = Message(tema=tema)

    def add_personaje(self, personaje: str):
        self.message.personaje = sanitize_attribute(personaje)
        return self
    
    def add_script(self, script: str):
        self.message.script = sanitize_attribute(script)
        return self
    
    def add_tts_audio_name(self, tts_audio_name: str):
        self.message.tts_audio_name = sanitize_attribute(tts_audio_name)
        return self
    
    def add_tts_audio_bucket(self, tts_audio_bucket: str):
        self.message.tts_audio_bucket = sanitize_attribute(tts_audio_bucket)
        return self
    
    def add_subtitles_name(self, subtitles_name: str):
        self.message.subtitles_name = sanitize_attribute(subtitles_name)
        return self
    
    def add_subtitles_bucket(self, subtitles_bucket: str):
        self.message.subtitles_bucket = sanitize_attribute(subtitles_bucket)
        return self
    
    def add_author(self, author: str):
        self.message.author = sanitize_attribute(author)
        return self
    
    def add_pitch(self, pitch: int):
        self.message.pitch = pitch
        return self
    
    def add_tts_voice(self, tts_voice: str):
        self.message.tts_voice = sanitize_attribute(tts_voice)
        return self
    
    def add_tts_rate(self, tts_rate: int):
        self.message.tts_rate = tts_rate
        return self
    
    def add_pth_voice(self, pth_voice: str):
        self.message.pth_voice = sanitize_attribute(pth_voice)
        return self
    
    def add_gameplay_name(self, gameplay_name: str):
        self.message.gameplay_name = sanitize_attribute(gameplay_name)
        return self

    def add_instagram_account(self, instagram_account:str):
        self.message.instagram_account = sanitize_attribute(instagram_account)
        return self
    
    def build(self):
        return self.message
