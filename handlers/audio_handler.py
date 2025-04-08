from file_getter.minio_file_getter import MinioFileGetter
from audio.audio import Audio

class AudioHandler:
    def get_audio(self, audio_bucket_name:str, audio_object_name:str, file_getter: MinioFileGetter ,temp_audio_folder) -> Audio:
        """Gets an audio from a minio Bucket

        Args:
            audio_bucket_name (str): The bucket name where the audio is stored
            audio_object_name (str): The name of the audio in the container
            file_getter (MinioFileGetter): Method to get the audio
            temp_audio_folder (str): Folder where the audio will be saved

        Returns:
            Audio: An instance of the created audio
        """
        audio_file_location = file_getter.get_file_temp_folder(temp_audio_folder, audio_object_name, audio_bucket_name)
        audio = Audio(audio_file_location, personaje=None)
        return audio



