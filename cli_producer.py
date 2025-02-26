from quixstreams import Application


def main():

    app_producer = Application(broker_address="localhost:9092", loglevel="DEBUG")


    with app_producer.get_producer() as producer:
        while True:
            input("Enviar mensaje de prueba: \n")
            data = {
    'status': 'OK',
    'subtitles_name': 'test_2025-02-26_10_48_47_517953.json',
    'bucket': 'subtitles-json'
}
            producer.produce(
                topic="subtitles-audios", key="cli_producer", value=str(data)
            )


if __name__ == "__main__":
    main()