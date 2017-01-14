#! /usr/bin/python
import unittest
from src.main import app_util


class AppUtilTestCase(unittest.TestCase):

    def test_load_data(self):
        data = app_util.load_data('fnames.txt')
        self.assertTrue(len(data) > 0)
        self.assertIsNotNone(data)

    def test_read_valid_conf(self):
        conf = app_util.read_conf('Kafka', 'hosts')
        self.assertIsNotNone(conf)

    def test_read_invalid_conf(self):
        conf = app_util.read_conf('InvalidSection', 'invalidItem')
        self.assertIsNone(conf)

    def test_read_invalid_conf_using_default_value(self):
        default_value = 'test'
        conf = app_util.read_conf('InvalidSection', 'invalidItem', default_value)
        self.assertEqual(conf, default_value)

    def test_get_template_folder(self):
        conf = app_util.get_template_folder()
        self.assertIsNotNone(conf)

    def test_get_static_folder(self):
        conf = app_util.get_static_folder()
        self.assertIsNotNone(conf)

if __name__ == '__main__':
    unittest.main()