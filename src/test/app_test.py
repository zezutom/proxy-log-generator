#! /usr/bin/python
import unittest
from src.main import app, app_util
from src.main.app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()

        # Propagate app exceptions to the test client
        self.app.testing = True

    def test_app_config(self):
        self.assertEqual(app.template_folder, app_util.get_template_folder())
        self.assertEqual(app.static_folder, app_util.get_static_folder())

    def test_homepage(self):
        res = self.app.get('/')
        assert '200' in res.status
