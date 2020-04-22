from .WebTestCase import WebTestCase
import flask

class TestRoutes(WebTestCase):

    def test_home_route_context(self):
        """ NOTE: I'm not totally sure what the difference between request_context and the client object are
                  I think the difference is that the test_client executes the request, 
                  while the request_context drops us into the server-side code as if we're making the request
                  Could be useful, leaving this in for reference/future use
        """
        with self.app.test_request_context('/'):
            assert flask.request.path == '/'

    def test_home_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/')
            assert rsp.content_type == 'text/html; charset=utf-8'
            assert rsp.status_code == 200

    def test_api_base_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/api/')
            assert rsp.content_type == 'application/json'
            assert rsp.status_code == 200

    def test_api_systems_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/api/systems')
            assert rsp.content_type == 'application/json'
            assert rsp.status_code == 200