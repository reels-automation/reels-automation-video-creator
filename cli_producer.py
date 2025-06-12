from quixstreams import Application


def main():

    app_producer = Application(broker_address="localhost:9092", loglevel="DEBUG")


    with app_producer.get_producer() as producer:
        while True:
            input("Enviar mensaje de prueba para crear el video: \n")
            data ={'tema': 'tema_at_1746766153.9746513', 'usuario': '51d64d7d-c2ce-4142-b7a9-5732c53c4818', 'idioma': 'en', 'personaje': 'Homero Simpson', 'script': 'i hate the ducks', 'audio_item': [{'tts_audio_name': 'tema_at_1746766153_9746513_2025-05-09_01_49_13_977408.mp3', 'tts_audio_directory': 'audios-tts', 'file_getter': 'minio', 'pitch': 0, 'tts_voice': 'en-NZ-MitchellNeural', 'tts_rate': 0, 'pth_voice': 'HOMERO SIMPSON LATINO'}], 'subtitle_item': [{'subtitles_name': 'tema_at_1746766153_9746513_2025-05-09_01_49_13_977408.json', 'file_getter': 'minio', 'subtitles_directory': 'subtitles-json'}], 'author': '', 'gameplay_name': 'subway.mp4', 'background_music': [{'audio_name': '', 'file_getter': '', 'start_time': 0, 'duration': 100}], 'images': [{'image_name': 'homero1.png', 'image_modifier': 'rotate', 'file_getter': 'local', 'image_directory': 'HOMERO SIMPSON LATINO', 'timestamp': 0, 'duration': 10}], 'random_images': True, 'random_amount_images': 5, 'gpt_model': 'llama3.2:3b'}
        
            producer.produce(
                topic="subtitles-audios", key="cli_producer", value=str(data)
            )


if __name__ == "__main__":
    main()
