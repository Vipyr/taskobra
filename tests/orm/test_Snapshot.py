# Testcase
from .ORMTestCase import ORMTestCase
# Libraries
from collections import defaultdict
from datetime import datetime, timedelta
from functools import reduce
from math import sqrt
from sqlalchemy import create_engine, Column, ForeignKey, Integer
import statistics
from typing import Collection
# Taskobra
from taskobra.orm import get_engine, get_session, Metric, Snapshot


class TestSnapshotMetric(Metric):
    __tablename__ = "TestSnapshotMetric"
    unique_id = Column(Integer, ForeignKey("Metric.unique_id"), primary_key=True)
    field = Column(Integer)
    __mapper_args__ = {
        "polymorphic_identity": __tablename__
    }

    @classmethod
    def prune(cls, metrics: Collection["TestSnapshotMetric"]):
        # print("pruning", metrics)
        by_field = defaultdict(list)
        [by_field[metric.field].append(metric) for metric in metrics]
        for field, metrics in by_field.items():
            # print(field, metrics)
            for metric in super().prune(metrics):
                metric.field = field
                # print("    yielding", metric)
                yield metric

    def __repr__(self):
        s = "<TestSnapshotMetric("
        s += f"field={self.field} ({self.mean:.3}"
        if self.sample_count > 1:
            s += f" sd:{self.standard_deviation:.3} {self.sample_count})"
        s += "))>"
        return s


class TestSnapshot(ORMTestCase):
    def test_prune(self):
        snapshots = [
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)], sample_rate=2.0),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 48), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 47), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
        ]

        print()
        for snapshot in snapshots:
            print(snapshot)
            [print(f"    {metric}") for metric in snapshot.metrics]

        pruned_snapshots = Snapshot.prune(datetime(2020, 3, 9, 9, 53, 53), snapshots)
        pruned_snapshots.append(
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 55), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]),
        )
        Snapshot.prune(datetime(2020, 3, 9, 9, 55, 57), pruned_snapshots)
