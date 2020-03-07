from .WebTestCase import WebTestCase
import flask

class TestRoutes(WebTestCase):

    def test_home_route(self):
        with self.app.test_request_context('/'):
            assert flask.request.path == '/'

    def test_api_base(self):
        with self.app.test_request_context('/api'):
            assert flask.request.path == '/api'
