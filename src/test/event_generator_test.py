#! /usr/bin/python
import re
import unittest
from datetime import datetime
from src.main import app_util, event_generator


class EventGeneratorTestCase(unittest.TestCase):

    def test_rand_ip(self):
        ip = event_generator.rand_ip()

        # There must be a new generated IP
        self.assertIsNotNone(ip)

        # The IP must be public
        self.assertFalse(re.match('^(10|127|169|172|192)\..*$', ip), 'Invalid IP %s' % ip)

        # The IP must be of v4
        octets = ip.split('.')
        self.assertEquals(4, len(octets))
        for octet in octets:
            self.assertTrue(1 <= int(octet) <= 255, 'Invalid octet value \'%s\'' % octet)

    def test_rand_user_agent(self):
        user_agent = event_generator.rand_user_agent()

        # There must be a new generated user agent
        self.assertIsNotNone(user_agent)

        # The generated agent must be one of the available user agents
        user_agents = map(lambda x: str(x).strip(), app_util.load_data('user_agents.txt'))
        self.assertTrue(user_agent in user_agents, 'Invalid user agent \'%s\'' % user_agent)

    def test_rand_auth(self):
        # An anonymous user
        self.assertEquals('-', event_generator.rand_auth(True))

        # Naming conventions: first_name.last_name
        username = event_generator.rand_auth(False)
        self.assertIsNotNone(username)
        (fname, lname) = username.split('.')
        self.assertIsNotNone(fname)
        self.assertIsNotNone(lname)

        # The generated username must match user records
        def f(x): return str(x).strip().lower()
        fnames = map(f, app_util.load_data('fnames.txt'))
        lnames = map(f, app_util.load_data('lnames.txt'))
        self.assertTrue(fname in fnames, 'Invalid first name \'%s\'' % fname)
        self.assertTrue(lname in lnames, 'Invalid last name \'%s\'' % lname)

    def test_rand_url(self):
        url = event_generator.rand_url()
        self.assertIsNotNone(url)

        # The url conforms to the expected format
        self.assertTrue(re.match('^http[s]?://www\.\w[-]?\w.*(jpg|png|html|xml|php|asp)$', url),
                        'Invalid URL \'%s\'' % url)

    def test_rand_http_status(self):
        status = event_generator.rand_http_status()
        self.assertTrue(status in map(lambda x: int(x),
                                      (200, 302, 404, 500, 502, 503)),
                        'Invalid HTTP status: %s' % status)

    def test_rand_res_size(self):
        size = event_generator.rand_res_size()
        self.assertTrue(1 <= size <= 5000000, 'Invalid resource size: %d' % size)

    def test_create_event(self):
        timestamp = datetime.now()
        event = event_generator.create_event(timestamp)
        self.assertIsNotNone(event, 'A valid event is expected')
        self.assertEquals(timestamp.strftime('%Y-%m-%d %H:%M:%S'), event['timestamp'])
        for p in ['ip', 'user_agent', 'authenticated', 'url', 'res_status', 'res_size']:
            self.assertIsNotNone(event[p])


if __name__ == '__main__':
    unittest.main()
