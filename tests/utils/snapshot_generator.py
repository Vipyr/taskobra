from collections import namedtuple
from unittest.mock import MagicMock, patch
from random import random, randint
import taskobra.monitor.__main__


def snapshot_generator():
    class Percent(float):
        def __repr__(self):
            return f"{self:.1f}"

    def mock_disk_usage(_):
        disk_usage = namedtuple("sdiskusage", ["total", "used", "free", "percent"])
        total = randint(1, 500000000000)
        used = randint(0, total)
        return disk_usage(total, used, total-used, Percent(100*used/total))

    with patch("taskobra.monitor.__main__.psutil") as mock_psutil:
        mock_psutil.disk_usage.side_effect = mock_disk_usage


        mock_psutil.virtual_memory.side_effect = lambda: 100 * random()
        mock_psutil.swap_memory.side_effect = lambda: 100 * random()
        mock_psutil.cpu_percent.side_effect = lambda: 100 * random()
        while True:
            yield taskobra.monitor.__main__.create_snapshot([])
