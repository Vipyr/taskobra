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
        t0 = datetime(2020, 3, 9, 9, 53)
        snapshots = [
            Snapshot(
                metrics=[
                    TestSnapshotMetric(field=0, mean=2.0),
                    TestSnapshotMetric(field=1, mean=4.0),
                ],
                sample_rate=2.0,
                timestamp=t0
            ),
            Snapshot(
                metrics=[
                    TestSnapshotMetric(field=0, mean=3.0),
                    TestSnapshotMetric(field=1, mean=5.0),
                ],
                timestamp=t0 - timedelta(seconds=2.0)
            ),
            Snapshot(
                metrics=[
                    TestSnapshotMetric(field=0, mean=2.5),
                    TestSnapshotMetric(field=1, mean=4.5),
                ],
                timestamp=t0 - timedelta(seconds=5.0)
            ),
            Snapshot(
                metrics=[
                    TestSnapshotMetric(field=0, mean=2.5),
                    TestSnapshotMetric(field=1, mean=4.5),
                ],
                timestamp=t0 - timedelta(seconds=3.0)
            ),
        ]

        print()
        for snapshot in snapshots:
            print(snapshot)
            [print(f"    {metric}") for metric in snapshot.metrics]

        print("Pruned:")
        snapshot = Snapshot.prune(t0, snapshots)
        # print("Pruned:")
        # snapshot = Snapshot.prune(t0 - timedelta(seconds=1), snapshots)
        # print(snapshot)
        # [print(f"    {metric}") for metric in snapshot.metrics]

        class SnapshotMock:
            def __init__(self, t, rate, base):
                self.t = t
                self.rate = rate
                self.base = base

            def __repr__(self):
                return f"({self.t}, {self.rate}, {self.base})"

        ts = [
            # SnapshotMock(0.0, 1.0, 2.0),
            # SnapshotMock(1.0, 1.0, 2.0),
            SnapshotMock(3.0, 1.0, 2.0),
            SnapshotMock(4.0, 1.0, 3.0),
            SnapshotMock(5.0, 1.0, 2.0),
            SnapshotMock(6.0, 1.0, 2.0),
            SnapshotMock(7.0, 1.0, 2.0),
            SnapshotMock(8.0, 1.0, 2.0),
            SnapshotMock(9.0, 1.0, 2.0),
            SnapshotMock(10.0, 1.0, 2.0),
            SnapshotMock(11.0, 1.0, 2.0),
            SnapshotMock(12.0, 1.0, 2.0),
            SnapshotMock(13.0, 1.0, 2.0),
            SnapshotMock(14.0, 1.0, 2.0),
            SnapshotMock(2.0, 1.0, 2.0),
            SnapshotMock(15.0, 1.0, 2.0),
            SnapshotMock(16.0, 1.0, 2.0),
        ]

        prunes = []
        time_slice = None
        exp = 1
        rate = None
        base = None
        snaps = []
        for sm in sorted(ts, key=lambda snap: snap.t):
            if  rate is not None and base is not None and time_slice[0] <= sm.t < time_slice[1]:
                rate = (rate * len(snaps) + sm.rate) / (len(snaps) + 1)
                base = (base * len(snaps) + sm.base) / (len(snaps) + 1)
                time_slice = (time_slice[0], time_slice[0] + rate * base ** exp)
            elif snaps:
                prunes.append((time_slice, snaps))
                snaps = []
                exp += 1
                rate = sm.rate
                base = sm.base
                time_slice = (time_slice[1], time_slice[1] + rate * base ** exp)
            else:
                rate = sm.rate
                base = sm.base
                time_slice = (sm.t, sm.t + rate * base ** exp)
            snaps.append(sm)
        prunes.append((time_slice, snaps))

        # [print(snaps) for snaps in prunes]
