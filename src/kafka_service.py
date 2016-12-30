from time import sleep

from kafka import KafkaConsumer


class KafkaService:
    def __init__(self):
        pass

    @staticmethod
    def stream_event(topic):
        for msg in KafkaConsumer(topic):
            # Wait to give a client a chance to react
            # Randomise the sleep to ensure data variety
            sleep(0.5)

            # Stream the new message
            yield "data: {}\n\n".format(msg.value)
