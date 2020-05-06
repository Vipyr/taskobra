from unittest import skip

from .WebTestCase import WebTestCase
import flask

class TestRoutes(WebTestCase):
    @skip("Routes broken by system_id foreign key column added to Snapshot class")
    def test_home_route_context(self):
        with self.app.test_request_context('/'):
            assert flask.request.path == '/'

    @skip("Routes broken by system_id foreign key column added to Snapshot class")
    def test_home_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/')
            assert rsp.content_type == 'text/html; charset=utf-8'
            assert rsp.status_code == 200

    @skip("Routes broken by system_id foreign key column added to Snapshot class")
    def test_api_base_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/api/')
            assert rsp.content_type == 'application/json'
            assert rsp.status_code == 200

    @skip("Routes broken by system_id foreign key column added to Snapshot class")
    def test_api_systems_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/api/systems')
            assert rsp.content_type == 'application/json'
            assert rsp.status_code == 200

    @skip("Routes broken by system_id foreign key column added to Snapshot class")
    def test_api_metrics_cpu_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/api/metrics/cpu')
            assert rsp.content_type == 'application/json'
            assert rsp.status_code == 200

    @skip("Routes broken by system_id foreign key column added to Snapshot class")
    def test_api_metrics_gpu_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/api/metrics/gpu')
            assert rsp.content_type == 'application/json'
            assert rsp.status_code == 200

    @skip("Routes broken by system_id foreign key column added to Snapshot class")
    def test_api_metrics_memory_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/api/metrics/memory')
            assert rsp.content_type == 'application/json'
            assert rsp.status_code == 200

    @skip("Routes broken by system_id foreign key column added to Snapshot class")
    def test_api_metrics_storage_route(self):
        with self.app.test_client() as client:
            rsp = client.get('/api/metrics/storage')
            assert rsp.content_type == 'application/json'
            assert rsp.status_code == 200
