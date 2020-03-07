from unittest import TestCase
from taskobra.web import create_app


class WebTestCase(TestCase):
    def setUp(self):
        self.app = create_app(config="DEBUG") # TODO: Update when configs are a thing

    def tearDown(self):
        self.app = None
