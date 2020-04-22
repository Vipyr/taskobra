from unittest import TestCase
from taskobra.web import create_app


class WebTestCase(TestCase):
    def setUp(self):
        self.app = create_app()

    def tearDown(self):
        self.app = None
