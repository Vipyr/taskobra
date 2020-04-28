from collections import defaultdict
from sqlalchemy import Column, ForeignKey, Integer
from typing import Collection
from taskobra.orm.metrics.metric import Metric


class CpuPercent(Metric):
    __tablename__ = "CpuPercent"
    unique_id = Column(Integer, ForeignKey("Metric.unique_id"), primary_key=True)
    core_id = Column(Integer)
    __mapper_args__ = {
        "polymorphic_identity": __tablename__
    }

    @classmethod
    def prune(cls, metrics: Collection["TestSnapshotMetric"]):
        by_core_id = defaultdict(list)
        [by_core_id[metric.core_id].append(metric) for metric in metrics]
        for core_id, metrics in by_core_id.items():
            for metric in super().prune(metrics):
                metric.core_id = core_id
                yield metric

    def __repr__(self):
        s = f"<Cpu{self.core_id}Percent({100*self.mean:.1f}"
        if self.sample_count > 1:
            s += f" sd:{self.standard_deviation:.3} {self.sample_count})"
        s += ")>"
        return s
