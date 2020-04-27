from unittest.mock import patch
import taskobra.monitor


@patch("taskobra.monitor.psutil")
def snapshot_generator(mock_psutil):
    mock_psutil.disk_usage.__call__ = random.random(0, 100)
    yield taskobra.monitor.create_snapshot([])
