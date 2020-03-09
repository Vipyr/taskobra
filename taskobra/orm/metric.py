# Libraries
from functools import reduce
import math
from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from typing import Collection
# Taskobra
from taskobra.orm.base import ORMBase


class Metric(ORMBase):
    __tablename__ = "Metric"
    unique_id = Column(Integer, primary_key=True)
    sample_count = Column(Integer, default=1)
    mean = Column(Float)
    variance = Column(Float, default=0.0)
    metric_type = Column(Enum(
        "TestMetricMetric",
        "TestSnapshotMetric",
    ))

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
        "polymorphic_on": metric_type,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "variance" not in kwargs:
            self.variance = type(self).variance.default.arg
        if "sample_count" not in kwargs:
            self.sample_count = type(self).sample_count.default.arg

    @property
    def standard_deviation(self):
        return math.sqrt(self.variance)

    @classmethod
    def prune(cls, metrics: Collection["Metric"]):
        if len(metrics) == 0:
            yield None
        if len(metrics) == 1:
            yield metrics[0]
        else:
            yield reduce(cls.merge, metrics)

    @classmethod
    def merge(cls, lhs: "Metric", rhs: "Metric"):
        if lhs is None:
            sample_count=rhs.sample_count
            mean=rhs.mean
            variance=rhs.variance
        else:
            # Compute the new count, mean, and variance
            # New count is just the sum of the two
            sample_count = lhs.sample_count + rhs.sample_count
            # New mean is the sum of the old sums divided by the new count
            mean = (lhs.mean * lhs.sample_count + rhs.mean * rhs.sample_count) / sample_count
            # Variance is the sum of the squares of all values divided by the count,
            # minus the square of the mean.
            # The new variance can be computed by recalculating the old sum of squares,
            # adding them, dividing that by the new count, and finally subtracting
            # the square of the new mean.
            lhs_square_sum = lhs.variance + lhs.mean ** 2
            rhs_square_sum = rhs.variance + rhs.mean ** 2
            square_sum = (lhs_square_sum * lhs.sample_count + rhs_square_sum * rhs.sample_count) / sample_count
            variance = square_sum - (mean ** 2)
        return cls(sample_count=sample_count, mean=mean, variance=variance)
