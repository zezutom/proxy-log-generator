import unittest
import mock
from src.main.kafka_consumer import KafkaConsumer


class KafkaConsumerTestCase(unittest.TestCase):
    @mock.patch('src.main.kafka_consumer.sleep')
    @mock.patch("src.main.kafka_consumer.KafkaClient")
    def test_kafka_consumer(self, mock_kafka_client, mock_sleep):

        # Init
        kafka_consumer = KafkaConsumer()
        test_topic = 'test_topic'
        test_subscriber_id = 'test_subscriber_id'

        # Make Kafka return a fake event
        class KafkaEvent(object):
            pass

        test_event = KafkaEvent()
        test_event.value = 'test'

        # Create a mock Kafka consumer as an iterator over fake events
        def __get_mock_consumer():
            return iter([test_event])

        def register():
            subscriber_id = kafka_consumer.register()
            self.assertIsNotNone(subscriber_id)

        def subscribe():
            event_generator = kafka_consumer.subscribe(test_subscriber_id, test_topic)
            self.assertIsNotNone(event_generator)
            # TODO verify the Kafka client's consumer has been passed as the 1st argument

        def consume_events():
            # Invoke the generator
            event_generator = kafka_consumer.consume_events(__get_mock_consumer(), test_subscriber_id, test_topic)
            data = next(event_generator)

            # Verify the returned result
            self.assertEqual(data, 'data: {0}\n\n'.format(test_event.value))

            # Verify the client got a chance to react to the streamed data
            mock_sleep.assert_called_with(1)

        @unittest.expectedFailure
        def consume_events_client_with_failure():
            # Invoke the generator
            event_generator = kafka_consumer.consume_events(__get_mock_consumer(), test_subscriber_id, 'invalid_topic')
            next(event_generator)
            self.fail('The call was expected to fail!')

        register()
        subscribe()
        consume_events()
        consume_events_client_with_failure()

if __name__ == '__main__':
    unittest.main()
