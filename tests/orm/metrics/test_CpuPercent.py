from ..ORMTestCase import ORMTestCase
from sqlalchemy import Column, ForeignKey, Integer
import statistics
from taskobra.orm import get_engine, get_session
from taskobra.orm.metrics import CpuPercent


class TestCpuPercent(ORMTestCase):
    def test_prune(self):
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            session.add(CpuPercent(core_id=0, mean=2))
            session.add(CpuPercent(core_id=0, mean=3))
            session.add(CpuPercent(core_id=1, mean=4))
            session.add(CpuPercent(core_id=1, mean=4))
            session.add(CpuPercent(core_id=1, mean=5))
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            metrics = list(session.query(CpuPercent))

            core0, core1 = CpuPercent.prune(metrics)
            self.assertAlmostEqual(core0.mean, statistics.mean((2, 3)), places=10)
            self.assertAlmostEqual(core0.variance, statistics.pvariance((2, 3)), places=10)
            self.assertEqual(core0.sample_count, 2)
            self.assertAlmostEqual(core1.mean, statistics.mean((4, 4, 5)), places=10)
            self.assertAlmostEqual(core1.variance, statistics.pvariance((4, 4, 5)), places=10)
            self.assertEqual(core1.sample_count, 3)
