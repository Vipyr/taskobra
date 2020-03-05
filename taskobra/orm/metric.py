# Libraries
import math
from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from typing import Collection
# Taskobra
from taskobra.orm.base import ORMBase


def combinatorial_mean_and_variance(l_mean, l_variance, l_N, r_mean, r_variance, r_N):
    N = l_N + r_N
    mean = (l_mean * l_N + r_mean * r_N) / N
    l_square_sum = l_variance + l_mean ** 2
    r_square_sum = r_variance + r_mean ** 2
    square_sum = (l_square_sum * l_N + r_square_sum * r_N) / N
    variance = square_sum - (mean ** 2)
    return mean, variance


class PruneStats:
    def __init__(self):
        self.mean = None
        self.variance = None
        self.sample_count = 0

    def add(self, metric: "Metric"):
        if self.mean is None:
            self.mean = metric.value
            self.variance = metric.variance
            self.sample_count = metric.sample_count
        else:
            self.mean, self.variance = combinatorial_mean_and_variance(
                self.mean,
                self.variance,
                self.sample_count,
                metric.value,
                metric.variance,
                metric.sample_count
            )
            self.sample_count += metric.sample_count


class Metric(ORMBase):
    __tablename__ = "Metric"
    unique_id = Column(Integer, primary_key=True)
    value = Column(Float)
    variance = Column(Float, default=0)
    sample_count = Column(Integer, default=1)
    metric_type = Column(Enum(
        "DummyMetric",
    ))

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
        "polymorphic_on": metric_type,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "variance" not in kwargs:
            self.variance = 0.0
        if "sample_count" not in kwargs:
            self.sample_count = 1

    @classmethod
    def prune(cls, dummies: Collection["Metric"]):
        stats = PruneStats()
        [stats.add(dummy) for dummy in dummies]
        return cls(
            value=stats.mean,
            variance=stats.variance,
            sample_count=stats.sample_count,
        )

    @property
    def standard_deviation(self):
        return math.sqrt(self.variance)
