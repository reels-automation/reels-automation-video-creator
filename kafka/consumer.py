import ast
from quixstreams import Application


def create_consumer(app_consumer: Application, topic_to_subscribe: str) -> str:
    with app_consumer.get_consumer() as consumer:
        consumer.subscribe([topic_to_subscribe])
        while True:
            msg = consumer.poll(1)
            if msg is None:
                print("Waiting...")
            elif msg.error() is not None:
                raise ValueError(msg.error())
            else:
                print("Message Value: ", msg.value())
                consumer.store_offsets(msg)
                msg_value_json_response = ast.literal_eval(msg.value().decode("utf-8"))
                return msg_value_json_response


