import json
import unittest

from src.main.push_server import app


class PushServerTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()

        # Propagate app exceptions to the test client
        self.app.testing = True

    def test_client_registration(self):
        res = self.app.get('/register')
        assert '200' in res.status
        data = json.loads(res.data)

        assert 'client_id' in data
        assert data['client_id'] is not None

        assert 'success' in data
        assert data['success'] is True

    def test_cancel_subscription(self):
        res = self.app.get('/register')
        data = json.loads(res.data)
        res = self.app.get('/cancel/{0}/test_topic'.format(data['client_id']))

        assert '200' in res.status
        data = json.loads(res.data)

        assert 'success' in data
        assert data['success'] is True

    def test_cancel_subscription_invalid_client_id(self):
        res = self.app.get('/cancel/fake_id/test_topic')
        assert '200' in res.status
        data = json.loads(res.data)

        assert 'success' in data
        assert data['success'] is False

        assert 'msg' in data
        self.assertEqual(data['msg'], 'Invalid client id')

    # TODO: test streaming using a mock Kafka client

if __name__ == '__main__':
    unittest.main()
