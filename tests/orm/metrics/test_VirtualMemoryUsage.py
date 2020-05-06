from ..ORMTestCase import ORMTestCase
from sqlalchemy import Column, ForeignKey, Integer
import statistics
from taskobra.orm import get_engine, get_session
from taskobra.orm.metrics import VirtualMemoryUsage


class TestCpuPercent(ORMTestCase):
    def test_prune(self):
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            session.add(VirtualMemoryUsage(total=10, mean=2))
            session.add(VirtualMemoryUsage(total=10, mean=3))
            session.add(VirtualMemoryUsage(total=10, mean=4))
            session.add(VirtualMemoryUsage(total=10, mean=4))
            session.add(VirtualMemoryUsage(total=10, mean=5))
