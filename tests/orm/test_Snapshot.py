# Testcase
from .ORMTestCase import ORMTestCase
# Libraries
from collections import defaultdict
from datetime import datetime
from itertools import chain
from math import log
from random import shuffle
from sqlalchemy import Column, ForeignKey, Integer
from typing import Collection
from unittest import skip
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

    def test_merge_commutative_property(self):
        snapshot0 = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 52), metrics=[TestSnapshotMetric(field=0, mean=2.0)])
        snapshot1 = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=4.0)])
        expected = Snapshot(
            timestamp=datetime(2020, 3, 9, 9, 53, 51),
            metrics=[TestSnapshotMetric(field=0, mean=3.0, sample_count=2, variance=1.0)],
            sample_count=2,
            sample_exponent=log(3.0, 2),
        )
        self.assertEqual(expected, snapshot0.merge(snapshot1))
        self.assertEqual(expected, snapshot1.merge(snapshot0))

    def test_merge_associative_property(self):
        snapshot0 = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)])
        snapshot1 = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)])
        snapshot2 = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 48), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)])
        merge_01_2 = snapshot0.merge(snapshot1).merge(snapshot2)
        merge_0_12 = snapshot0.merge(snapshot1.merge(snapshot2))
        self.assertEqual(merge_01_2.t_start, snapshot2.t_start)
        self.assertEqual(merge_01_2.t_end, snapshot0.t_end)
        self.assertEqual(merge_01_2.sample_count, merge_0_12.sample_count)
        self.assertEqual(merge_01_2.sample_rate, merge_0_12.sample_rate)
        self.assertEqual(merge_01_2.sample_base, merge_0_12.sample_base)
        self.assertEqual(merge_01_2.sample_exponent, merge_0_12.sample_exponent)
        self.assertEqual(merge_01_2.timestamp, merge_0_12.timestamp)
        self.assertEqual(merge_01_2, merge_0_12)

    def test_merge_identity_property(self):
        snapshot = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)])
        identity = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), sample_count=0)
        merge = snapshot.merge(identity)
        self.assertEqual(snapshot, merge)

    # @skip("Pruning Algorithm Still In Progress")
    def test_prune(self):
        snapshots = [
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)], sample_rate=2.0),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 48), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]),
        ]
        [print(item) for item in Snapshot.prune(sorted(snapshots, key=lambda snap: snap.timestamp))]
        return




        snapshots = [
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)], sample_rate=2.0),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 48), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 47), metrics=[TestSnapshotMetric(field=0, mean=3.5), TestSnapshotMetric(field=1, mean=5.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 40), metrics=[TestSnapshotMetric(field=0, mean=4.5), TestSnapshotMetric(field=1, mean=6.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 35), metrics=[TestSnapshotMetric(field=0, mean=5.5), TestSnapshotMetric(field=1, mean=7.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 29), metrics=[TestSnapshotMetric(field=0, mean=6.5), TestSnapshotMetric(field=1, mean=8.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 28), metrics=[TestSnapshotMetric(field=0, mean=7.5), TestSnapshotMetric(field=1, mean=9.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 27), metrics=[TestSnapshotMetric(field=0, mean=8.5), TestSnapshotMetric(field=1, mean=1.5)]),
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
        pruned_0_6 = Snapshot.prune(datetime(2020, 3, 9, 9, 53, 53), sorted(snapshots[:7]))
        print("Pruned:")
        for snapshot in pruned_0_6:
            print(snapshot)
            [print(f"    {metric}") for metric in snapshot.metrics]

        print()
        # pruned_7_13.append(Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 55), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]))
        pruned_7_13 = Snapshot.prune(datetime(2020, 3, 9, 9, 53, 53), sorted(snapshots[7:]))
        print("Pruned:")
        for snapshot in pruned_7_13:
            print(snapshot)
            [print(f"    {metric}") for metric in snapshot.metrics]

        # Make sure that pruning the result of a prune doesn't change it
        print()
        pruned_all = Snapshot.prune(datetime(2020, 3, 9, 9, 53, 53), sorted(snapshots))
        print("Pruned:")
        for snapshot in pruned_all:
            print(snapshot)
            [print(f"    {metric}") for metric in snapshot.metrics]
        # self.assertEqual(pruned_all, Snapshot.prune(datetime(2020, 3, 9, 9, 53, 53), pruned_all))

        # Make sure that pruning [:7] + [7:] yields the same results as pruning all of the snapshots
        self.assertEqual(
            Snapshot.prune(datetime(2020, 3, 9, 9, 53, 53), pruned_0_6 + pruned_7_13),
            pruned_all,
        )
