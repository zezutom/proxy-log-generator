import unittest
from mock import patch
from push_server import app

class PushServerTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()

        # Propagate app exceptions to the test client
        self.app.testing = True

    @patch('push_server.app.kafka_service')
    def test_streaming(self, mock_kafka_service):
        for sub in (
                {'url': '/stream/auth', 'topic': 'success_auth_logs'},
                {'url': '/stream/anon', 'topic': 'success_anon_logs'},
                {'url': '/stream/err', 'topic': 'err_logs'}):
            res = self.app.get(sub['url'])
            assert '200' in res.status
            mock_kafka_service.stream_event.assert_called_with(sub['topic'])


if __name__ == '__main__':
    unittest.main()
