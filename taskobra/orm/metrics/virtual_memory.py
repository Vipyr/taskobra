from collections import defaultdict
from sqlalchemy import Column, Float, ForeignKey, Integer
from typing import Collection
from taskobra.orm.metrics.metric import Metric


class VirtualMemoryUsage(Metric):
    __tablename__ = "VirtualMemoryUsage"
    unique_id = Column(Integer, ForeignKey("Metric.unique_id"), primary_key=True)
    total = Column(Float)
    __mapper_args__ = {
        "polymorphic_identity": __tablename__
    }

    @property
    def used(self):
        return self.mean

    @property
    def percent(self):
        return self.used / self.total

    def __repr__(self):
        s = f"<VirtualMemoryUsage({int(self.used)}/{int(self.total)}: {100*self.percent:.1f}"
        if self.sample_count > 1:
            s += f" sd:{self.standard_deviation:.3} {self.sample_count})"
        s += ")>"
        return s
