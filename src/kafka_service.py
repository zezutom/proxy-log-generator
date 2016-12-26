from kafka import KafkaConsumer
from time import sleep
from random import randrange

class KafkaService:
    def __init__(self):
        pass

    def stream_event(self, topic):
        for msg in KafkaConsumer(topic):
            # Wait to give a client a chance to react
            # Randomise the sleep to ensure data variety
            sleep(randrange(1, 5))

            # Stream the new message
            yield "data: {}\n\n".format(msg.value)
