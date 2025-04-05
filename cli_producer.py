from quixstreams import Application


def main():

    app_producer = Application(broker_address="localhost:9092", loglevel="DEBUG")


    with app_producer.get_producer() as producer:
        while True:
            input("Enviar mensaje de prueba para crear el video: \n")
            data ={
        "tema": "Mensaje de prueba",
        "personaje": "Homero Simpson",
        "script": "",
        "tts_audio_name": "gallego_troll_2025-04-02_09_19_19_357196.mp3",
        "tts_audio_bucket": "audios-tts",
        "subtitles_name": "gallego_troll_2025-04-02_09_19_19_357196.json",
        "subtitles_bucket": "subtitles-json",
        "author": "Mi amigo el galofa",
        "pitch": "0",
        "tts_voice": "es-ES-XimenaNeural",
        "tts_rate": "0",
        "pth_voice": "HOMERO SIMPSON LATINO",
        "instagram_account": "aprendiendo.con.personajes",
        "gameplay_name": "subway3.mp4"
    }
        
            producer.produce(
                topic="subtitles-audios", key="cli_producer", value=str(data)
            )


if __name__ == "__main__":
    main()