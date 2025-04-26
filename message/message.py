from dataclasses import dataclass,field
from utils.utils import sanitize_attribute
from datetime import datetime

@dataclass
class Message:
    tema: str
    usuario: str =""
    idioma:str=""
    personaje:str=""
    script: str=""
    audio_item:list= field(default_factory=list)
    subtitle_item:list=field(default_factory=list)
    author:str=""
    gameplay_name:str=""
    background_music:list= field(default_factory=list)
    images:list= field(default_factory=list)
    random_images:str="false"
    random_amount_images:int=0
    gpt_model:str=""
    

    def to_dict(self):
        return self.__dict__
    
    def get_pth_voice(self):
        return self.audio_item[0]["pth_voice"]
    
    def set_pth_voice(self, new_pth_voice:str):
        self.audio_item[0]["pth_voice"] = new_pth_voice
    
    def get_audio_bucket(self)-> str:
        return self.audio_item[0]["tts_audio_directory"]
    
    def get_audio_name(self)-> str:
        return self.audio_item[0]["tts_audio_name"]
    
    def get_subtitle_name(self)->str:
        return self.subtitle_item[0]["subtitles_name"]

    def get_subtitles_directory(self)->str:
        return self.subtitle_item[0]["subtitles_directory"]

    def are_images_random(self)->bool:
        if self.random_images == "false":
            return False        
        return True

    def get_video_name(self)->str:
        if len(self.tema) > 0:
            return self.tema
        return f"nameless_video_{datetime.now()}"

class MessageBuilder:
    def __init__(self, tema: str):
        self.message = Message(tema=tema)

    def add_usuario(self, usuario:str):
        self.message.usuario = sanitize_attribute(usuario)
        return self
    
    def add_idioma(self, idioma:str):
        self.message.idioma = idioma
        return self
    
    def add_personaje(self, personaje: str):
        self.message.personaje = sanitize_attribute(personaje)
        return self
    
    def add_script(self, script: str):
        self.message.script = sanitize_attribute(script)
        return self
    
    def add_audio_item(self,audio_item:list):
        self.message.audio_item = audio_item
        return self
    
    def add_subtitle_item(self,subtitle_item:list):
        self.message.subtitle_item = subtitle_item
        return self
    
    def add_author(self, author:str):
        self.message.author = author
        return self
    
    def add_gameplay_name(self, gameplay_name:str):
        self.message.gameplay_name = gameplay_name
        return self
    
    def add_background_music(self, background_music:list):
        self.message.background_music = background_music
        return self
    
    def add_images(self, images:list):
        self.message.images = images
        return self
    
    def add_random_images(self, random_images:str):
        self.message.random_images = random_images
        return self
    
    def add_random_amount_images(self, random_amount_images:int):
        self.message.random_amount_images = random_amount_images
        return self

    def add_gpt_model(self, gpt_model:str):
        self.message.gpt_model = gpt_model
        return self

    def build(self):
        return self.message