#! /usr/bin/python
import unittest
import mock
from mock import MagicMock
import json
from src.main.push_server import app


class PushServerTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()

        # Propagate app exceptions to the test client
        self.app.testing = True

    @mock.patch('src.main.push_server.KafkaConsumer')
    def test_push_server(self, mock_kafka_consumer):
        mock_kafka_consumer_instance = mock_kafka_consumer.return_value

        def register():
            subscriber_id = 'test_subscriber_id'
            mock_kafka_consumer_instance \
                .register \
                .return_value = subscriber_id

            res = self.app.get('/register')
            self.__assert_success_response(res,
                                           ('subscriber_id', subscriber_id),
                                           ('success', True))

        def subscribe():
            mock_kafka_consumer_instance \
                .subscribe \
                .return_value = MagicMock()
            res = self.app.get('/subscribe/test_subscriber_id/test_topic')
            self.__assert_success_response(res)
            self.assertEqual(res.mimetype, 'text/event-stream')

        def unsubscribe():
            mock_kafka_consumer_instance \
                .unsubscribe \
                .return_value = True
            res = self.app.get('/unsubscribe/test_subscriber_id/test_topic')
            self.__assert_success_response(res, ('success', True))

        def unsubscribe_failure():
            subscriber_id = 'test_subscriber_id'
            mock_kafka_consumer_instance \
                .unsubscribe \
                .return_value = False
            res = self.app.get('/unsubscribe/{0}/test_topic'.format(subscriber_id))
            self.__assert_success_response(res,
                                           ('success', False),
                                           ('subscriber_id', subscriber_id),
                                           ('msg', 'Invalid subscriber id'))

        register()
        subscribe()
        unsubscribe()
        unsubscribe_failure()

    def __assert_success_response(self, res, *props):
        assert '200' in res.status
        if props:
            data = json.loads(res.data)
            for (key, value) in props:
                assert key in data
                self.assertEqual(data[key], value)

if __name__ == '__main__':
    unittest.main()
