from .ORMTestCase import ORMTestCase
from functools import reduce
from math import sqrt
from sqlalchemy import create_engine, Column, ForeignKey, Integer
import statistics
from taskobra.orm import get_engine, get_session, Metric


class DummyMetric(Metric):
    __tablename__ = "DummyMetric"
    unique_id = Column(Integer, ForeignKey("Metric.unique_id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": __tablename__
    }

    def __repr__(self):
        return f"<DummyMetric({self.value:.3} sd:{self.variance:.3} ({self.sample_count})>"


class TestMetric(ORMTestCase):
    def test_Polymorphism(self):
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            session.add(DummyMetric(value=2))
            session.add(DummyMetric(value=3))
            session.add(DummyMetric(value=4))
            session.add(DummyMetric(value=4))
            session.add(DummyMetric(value=5))
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            dummies = list(session.query(Metric))

            prune1 = DummyMetric.prune(dummies[:3])
            self.assertAlmostEqual(prune1.value, statistics.mean((2, 3, 4)), places=10)
            self.assertAlmostEqual(prune1.variance, statistics.pvariance((2, 3, 4)), places=10)
            self.assertEqual(prune1.sample_count, 3)

            prune2 = DummyMetric.prune(dummies[3:])
            self.assertAlmostEqual(prune2.value, statistics.mean((4, 5)), places=10)
            self.assertAlmostEqual(prune2.variance, statistics.pvariance((4, 5)), places=10)
            self.assertEqual(prune2.sample_count, 2)

            prune3 = DummyMetric.prune((prune1, prune2))
            self.assertAlmostEqual(prune3.value, statistics.mean((2, 3, 4, 4, 5)), places=10)
            self.assertAlmostEqual(prune3.variance, statistics.pvariance((2, 3, 4, 4, 5)), places=10)
            self.assertEqual(prune3.sample_count, 5)
