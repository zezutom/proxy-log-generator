import re
import unittest
from datetime import timedelta

import log_generator


class LogGeneratorTestCase(unittest.TestCase):
    def test_default_options(self):
        options = log_generator.read_options()

        # There must be a default config
        self.assertIsNotNone(options)

        # A default path to the log file
        self.assertEquals("logfile.log", options.logfile, 'Invalid default log file location \'%s\'' % options.logfile)

        # A default time range is 2 days
        self.assertEquals('2d', options.duration, 'Invalid default time range: %s' % options.duration)

        # There are new log events every 5 minutes
        self.assertEquals(5, options.increment, 'Invalid default increment: %d' % options.increment)

    def test_parse_duration(self):
        days = timedelta(days=10)
        self.verify_time_options(days, self.parse_time_options('10d'))
        self.verify_time_options(days, self.parse_time_options('10D'))

        hours = timedelta(hours=3)
        self.verify_time_options(hours, self.parse_time_options('3h'))
        self.verify_time_options(hours, self.parse_time_options('3H'))

        minutes = timedelta(minutes=125)
        self.verify_time_options(minutes, self.parse_time_options('125m'))
        self.verify_time_options(minutes, self.parse_time_options('125M'))

        seconds = timedelta(seconds=59)
        self.verify_time_options(seconds, self.parse_time_options('59s'))
        self.verify_time_options(seconds, self.parse_time_options('59S'))

        self.verify_time_options(timedelta(days=2), self.parse_time_options('invalid entry'))

    def verify_time_options(self, expected, actual):
        self.assertEquals(expected, actual, 'Wrong time delta %s' % actual)

    @staticmethod
    def parse_time_options(duration_expr):
        options = log_generator.read_options()
        options.duration = duration_expr
        time_delta = log_generator.parse_duration(options)
        return time_delta

    def test_rand_ip(self):
        ip = log_generator.rand_ip()

        # There must be a new generated IP
        self.assertIsNotNone(ip)

        # The IP must be public
        self.assertFalse(re.match('^(10|127|169|172|192).*$', ip), 'Invalid IP %s' % ip)

        # The IP must be of v4
        octets = ip.split('.')
        self.assertEquals(4, len(octets))
        for octet in octets:
            self.assertTrue(1 <= int(octet) <= 255, 'Invalid octet value \'%s\'' % octet)

    def test_rand_user_agent(self):
        user_agent = log_generator.rand_user_agent()

        # There must be a new generated user agent
        self.assertIsNotNone(user_agent)

        # The generated agent must be one of the available user agents
        user_agents = map(lambda x: str(x).strip(), log_generator.read_conf('user_agents.txt'))
        self.assertTrue(user_agent in user_agents, 'Invalid user agent \'%s\'' % user_agent)

    def test_rand_auth(self):
        # An anonymous user
        self.assertEquals('-', log_generator.rand_auth(True))

        # Naming conventions: first_name.last_name
        username = log_generator.rand_auth(False)
        self.assertIsNotNone(username)
        (fname, lname) = username.split('.')
        self.assertIsNotNone(fname)
        self.assertIsNotNone(lname)

        # The generated username must match user records
        def f(x): return str(x).strip().lower()
        fnames = map(f, log_generator.read_conf('fnames.txt'))
        lnames = map(f, log_generator.read_conf('lnames.txt'))
        self.assertTrue(fname in fnames, 'Invalid first name \'%s\'' % fname)
        self.assertTrue(lname in lnames, 'Invalid last name \'%s\'' % lname)

    def test_rand_url(self):
        url = log_generator.rand_url()
        self.assertIsNotNone(url)

        # The url conforms to the expected format
        self.assertTrue(re.match('^http[s]?://www\.\w[-]?\w.*(jpg|png|html|xml|php|asp)$', url),
                        'Invalid URL \'%s\'' % url)

    def test_rand_http_status(self):
        status = log_generator.rand_http_status()
        self.assertTrue(status in map(lambda x: str(x), (200, 302, 404, 500)), 'Invalid HTTP status: %s' % status)

    def test_rand_res_size(self):
        size = log_generator.rand_res_size()
        self.assertTrue(1 <= size <= 5000000, 'Invalid resource size: %d' % size)


if __name__ == '__main__':
    unittest.main()
