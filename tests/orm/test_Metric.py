from .ORMTestCase import ORMTestCase
from functools import reduce
from math import sqrt
from sqlalchemy import create_engine, Column, ForeignKey, Integer
import statistics
from taskobra.orm import get_engine, get_session, Metric


class TestMetricMetric(Metric):
    __tablename__ = "TestMetricMetric"
    unique_id = Column(Integer, ForeignKey("Metric.unique_id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": __tablename__
    }

    def __repr__(self):
        if self.sample_count == 1:
            return f"<TestMetricMetric({self.mean:.3})>"
        return f"<TestMetricMetric({self.mean:.3} sd:{self.standard_deviation:.3} ({self.sample_count})>"


class TestMetric(ORMTestCase):
    def test_prune(self):
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            session.add(TestMetricMetric(mean=2))
            session.add(TestMetricMetric(mean=3))
            session.add(TestMetricMetric(mean=4))
            session.add(TestMetricMetric(mean=4))
            session.add(TestMetricMetric(mean=5))
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            dummies = list(session.query(Metric))

            prune1 = next(TestMetricMetric.prune(dummies[:3]))
            self.assertAlmostEqual(prune1.mean, statistics.mean((2, 3, 4)), places=10)
            self.assertAlmostEqual(prune1.variance, statistics.pvariance((2, 3, 4)), places=10)
            self.assertEqual(prune1.sample_count, 3)

            prune2 = next(TestMetricMetric.prune(dummies[3:]))
            self.assertAlmostEqual(prune2.mean, statistics.mean((4, 5)), places=10)
            self.assertAlmostEqual(prune2.variance, statistics.pvariance((4, 5)), places=10)
            self.assertEqual(prune2.sample_count, 2)

            prune3 = next(TestMetricMetric.prune((prune1, prune2)))
            self.assertAlmostEqual(prune3.mean, statistics.mean((2, 3, 4, 4, 5)), places=10)
            self.assertAlmostEqual(prune3.variance, statistics.pvariance((2, 3, 4, 4, 5)), places=10)
            self.assertEqual(prune3.sample_count, 5)
