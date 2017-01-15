#! /usr/bin/python

from pykafka import KafkaClient
from time import sleep
import uuid
import app_util


class KafkaConsumer:

    def __init__(self):
        # Instantiate a Kafka client
        self.kafka_client = KafkaClient(hosts=app_util.read_conf('Kafka', 'hosts', '127.0.0.1:9092'))

        # Client subscriptions to Kafka topics: client_id -> [ topic1, topic2, .. , topicN ]
        self.subscriptions = {}

    def consume_events(self, consumer, subscriber_id, topic):
        for e in consumer:
            if topic not in self.subscriptions[subscriber_id]:
                print 'Exiting the channel, subscription to \'{0}\' has been cancelled'.format(topic)
                break

            sleep(1)  # give the subscribed client a chance to react
            yield 'data: {0}\n\n'.format(e.value)

    def register(self):
        # Generate a random UUID
        subscriber_id = str(uuid.uuid4())

        # Initialise a topic queue and return the new id
        self.subscriptions[subscriber_id] = []
        return subscriber_id

    def subscribe(self, subscriber_id, topic):
        if subscriber_id not in self.subscriptions:
            self.subscriptions[subscriber_id] = []
        self.subscriptions[subscriber_id].append(topic)
        return self.consume_events(self.kafka_client.topics[topic].get_simple_consumer(), subscriber_id, topic)

    def unsubscribe(self, subscriber_id, topic):
        if subscriber_id not in self.subscriptions:
            return False
        self.subscriptions[subscriber_id].remove(topic)
        return True
