from kafka import KafkaConsumer
from time import sleep


class KafkaService:
    def __init__(self):
        pass

    def stream_event(self, topic):
        for msg in KafkaConsumer(topic):
            # Wait to give a client a chance to react
            sleep(1)

            # Stream the new message
            yield "data: {}\n\n".format(msg.value)
