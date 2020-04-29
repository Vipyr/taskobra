from collections import namedtuple
import datetime
from unittest.mock import MagicMock, patch
from random import random, randint
import taskobra.monitor.__main__


def snapshot_generator(max_snaphots=None):
    class Percent(float):
        def __repr__(self):
            return f"{self * 100:0.1f}"

        def __str__(self):
            return repr(self)

    def mock_disk_usage(*_, **__):
        disk_usage = namedtuple("sdiskusage", ["total", "used", "free", "percent"])
        total = randint(1, 500000000000)
        used = randint(0, total)
        return disk_usage(total, used, total-used, Percent(used/total))

    def mock_virtual_memory(*_, **__):
        virtual_memory = namedtuple("svmem", ["total", "available", "percent", "used", "free", "active", "inactive", "buffers", "cached", "shared", "slab",])
        total = randint(1, 35000000000)
        available = randint(0, total)
        percent = Percent(available/total)
        used = total - available
        free = randint(0, available)
        active = randint(0, used)
        inactive = used - active
        buffers = randint(0, used)
        cached = randint(0, used)
        shared = randint(0, used)
        slab = randint(0, used)
        return virtual_memory(total, available, percent, used, free, active, inactive, buffers, cached, shared, slab)

    def mock_swap_memory(*_, **__):
        swap_memory = namedtuple("sswap", ["total", "used", "free", "percent", "sin", "sout"])
        total = randint(1, 64000000000)
        used = randint(0, total)
        free = total - used
        percent = Percent(used/total)
        sin = randint(0, 100000000000)
        sout = randint(0, 100000000000)
        return swap_memory(total, used, free, percent, sin, sout)

    def mock_cpu_percent(*_, **__):
        return Percent(random())

    with patch("taskobra.monitor.__main__.psutil") as mock_psutil:
        mock_psutil.disk_usage.side_effect = mock_disk_usage
        mock_psutil.virtual_memory.side_effect = mock_virtual_memory
        mock_psutil.swap_memory.side_effect = mock_swap_memory
        mock_psutil.cpu_percent.side_effect = mock_cpu_percent

        def mock_now(start_time):
            while True:
                start_time -= datetime.timedelta(seconds=randint(1, 5) + (-0.5 + random()))
                yield start_time

        now_generator = mock_now(datetime.datetime.now())
        with patch("taskobra.monitor.__main__.datetime.datetime") as mock_datetime_datetime:
            mock_datetime_datetime.now.side_effect = lambda: next(now_generator)

            count = 0
            while not max_snaphots or count < max_snaphots:
                count += 1
                yield taskobra.monitor.__main__.create_snapshot([])
