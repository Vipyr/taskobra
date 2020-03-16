# Testcase
from .ORMTestCase import ORMTestCase
# Libraries
from collections import defaultdict
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer
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
        by_field = defaultdict(list)
        [by_field[metric.field].append(metric) for metric in metrics]
        for field, metrics in by_field.items():
            for metric in super().prune(metrics):
                metric.field = field
                yield metric

    def __repr__(self):
        s = "<TestSnapshotMetric("
        s += f"field={self.field} ({self.mean:.3}"
        if self.sample_count > 1:
            s += f" sd:{self.standard_deviation:.3} {self.sample_count})"
        s += "))>"
        return s


class TestSnapshot(ORMTestCase):
    def test_creation(self):
        snapshot = Snapshot()
        self.assertEqual(snapshot.sample_rate, Snapshot.sample_rate.default.arg)
        self.assertEqual(snapshot.sample_base, Snapshot.sample_base.default.arg)
        self.assertEqual(snapshot.sample_exponent, Snapshot.sample_exponent.default.arg)

    def test_prune(self):
        snapshots = [
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 48), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 47), metrics=[TestSnapshotMetric(field=0, mean=3.5), TestSnapshotMetric(field=1, mean=5.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 40), metrics=[TestSnapshotMetric(field=0, mean=4.5), TestSnapshotMetric(field=1, mean=6.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 35), metrics=[TestSnapshotMetric(field=0, mean=5.5), TestSnapshotMetric(field=1, mean=7.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 29), metrics=[TestSnapshotMetric(field=0, mean=6.5), TestSnapshotMetric(field=1, mean=8.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 28), metrics=[TestSnapshotMetric(field=0, mean=7.5), TestSnapshotMetric(field=1, mean=9.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 27), metrics=[TestSnapshotMetric(field=0, mean=8.5), TestSnapshotMetric(field=1, mean=1.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)], sample_rate=2.0),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 25), metrics=[TestSnapshotMetric(field=0, mean=9.5), TestSnapshotMetric(field=1, mean=2.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 20), metrics=[TestSnapshotMetric(field=0, mean=1.5), TestSnapshotMetric(field=1, mean=3.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53,  5), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53,  1), metrics=[TestSnapshotMetric(field=0, mean=3.5), TestSnapshotMetric(field=1, mean=5.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53,  0), metrics=[TestSnapshotMetric(field=0, mean=4.5), TestSnapshotMetric(field=1, mean=6.5)]),
        ]

        print()
        for snapshot in snapshots:
            print(snapshot)
            # [print(f"    {metric}") for metric in snapshot.metrics]

        print()
        pruned_snapshots = Snapshot.prune(datetime(2020, 3, 9, 9, 53, 53), snapshots)
        print("Pruned:")
        for snapshot in pruned_snapshots:
            print(snapshot)
            [print(f"    {metric}") for metric in snapshot.metrics]

        print()
        pruned_snapshots.append(Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 55), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]))
        pruned_snapshots = Snapshot.prune(datetime(2020, 3, 9, 9, 55, 57), pruned_snapshots)
        print("Pruned:")
        for snapshot in pruned_snapshots:
            print(snapshot)
            [print(f"    {metric}") for metric in snapshot.metrics]

        print()
        repruned_snapshots = Snapshot.prune(datetime(2020, 3, 9, 9, 55, 57), pruned_snapshots)
        print("Pruned:")
        for snapshot in repruned_snapshots:
            print(snapshot)
            [print(f"    {metric}") for metric in snapshot.metrics]