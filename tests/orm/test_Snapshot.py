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
        exp1 = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 52), sample_exponent=1, sample_count=0)
        snapshot0 = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 52), metrics=[TestSnapshotMetric(field=0, mean=2.0)])
        snapshot1 = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=4.0)])
        result01 = exp1.merge(snapshot0).merge(snapshot1)
        result10 = exp1.merge(snapshot1).merge(snapshot0)
        self.assertEqual(result01, result10)
        self.assertEqual(result01.sample_count, 2)
        self.assertEqual(result01.sample_rate, 1.0)
        self.assertEqual(result01.sample_base, 2.0)
        self.assertEqual(result01.sample_exponent, 1)
        self.assertEqual(len(result01.metrics), 1)
        self.assertEqual(result01.metrics[0].mean, 3.0)
        self.assertEqual(result01.metrics[0].standard_deviation, 1.0)
        self.assertEqual(result01.metrics[0].sample_count, 2)

    def test_merge_identity_property(self):
        identity = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), sample_count=0, sample_exponent=1)
        snapshot = Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)])
        merge = identity.merge(snapshot)

        self.assertEqual(merge.sample_count,                  snapshot.sample_count)
        self.assertEqual(merge.sample_rate,                   snapshot.sample_rate)
        self.assertEqual(merge.sample_base,                   snapshot.sample_base)
        self.assertEqual(merge.sample_exponent,               1)
        self.assertEqual(len(merge.metrics),                  len(snapshot.metrics))
        self.assertEqual(merge.metrics[0].mean,               snapshot.metrics[0].mean)
        self.assertEqual(merge.metrics[0].standard_deviation, snapshot.metrics[0].standard_deviation)
        self.assertEqual(merge.metrics[0].sample_count,       snapshot.metrics[0].sample_count)

    # @skip("rawr")
    def test_prune(self):
        # snapshots = [
        #     Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)], sample_rate=2.0),
        #     Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
        #     Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 48), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]),
        # ]
        # prune1 = [item for item in Snapshot.prune(reversed(sorted(snapshots, key=lambda snap: snap.timestamp)))]
        # prune2 = [item for item in prune1]
        # self.assertEqual(prune1, prune2)

        # print()
        # [print(s) for s in prune1]
        # self.assertLess(len(prune1), len(snapshots))

        snapshots = [
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53), metrics=[TestSnapshotMetric(field=0, mean=2.0), TestSnapshotMetric(field=1, mean=4.0)], sample_rate=2.0),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 50), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 48), metrics=[TestSnapshotMetric(field=0, mean=3.0), TestSnapshotMetric(field=1, mean=5.0)]),

            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 47), metrics=[TestSnapshotMetric(field=0, mean=3.5), TestSnapshotMetric(field=1, mean=5.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 40), metrics=[TestSnapshotMetric(field=0, mean=4.5), TestSnapshotMetric(field=1, mean=6.5)]),

            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 35), metrics=[TestSnapshotMetric(field=0, mean=5.5), TestSnapshotMetric(field=1, mean=7.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 29), metrics=[TestSnapshotMetric(field=0, mean=6.5), TestSnapshotMetric(field=1, mean=8.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 28), metrics=[TestSnapshotMetric(field=0, mean=7.5), TestSnapshotMetric(field=1, mean=9.5)], sample_rate=2.0),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 27), metrics=[TestSnapshotMetric(field=0, mean=8.5), TestSnapshotMetric(field=1, mean=1.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 25), metrics=[TestSnapshotMetric(field=0, mean=9.5), TestSnapshotMetric(field=1, mean=2.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 20), metrics=[TestSnapshotMetric(field=0, mean=1.5), TestSnapshotMetric(field=1, mean=3.5)]),

            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53,  5), metrics=[TestSnapshotMetric(field=0, mean=2.5), TestSnapshotMetric(field=1, mean=4.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53,  1), metrics=[TestSnapshotMetric(field=0, mean=3.5), TestSnapshotMetric(field=1, mean=5.5)]),
            Snapshot(timestamp=datetime(2020, 3, 9, 9, 53,  0), metrics=[TestSnapshotMetric(field=0, mean=4.5), TestSnapshotMetric(field=1, mean=6.5)]),
        ]
        sorted_snapshots = list(reversed(sorted(snapshots, key=lambda snap: snap.timestamp)))
        pruned = [item for item in Snapshot.prune(sorted_snapshots)]
        self.assertLess(len(pruned), len(snapshots))

        # # Assert that pruning the same data twice yields the same result
        # print()
        # print("Prune Twice")
        # prune1 = [item for item in Snapshot.prune(sorted_snapshots)]
        # self.assertEqual(pruned, prune1)

        # # Assert that pruning the result of a prune yields the same result
        # print()
        # print("Prune Again")
        # prune1 = [item for item in Snapshot.prune(pruned)]
        # self.assertEqual(pruned, prune1)

        prune1 = []
        for i in reversed(range(len(snapshots)-1)):
            print()
            print("Prune Incremental", i)
            prune1 = [item for item in Snapshot.prune(
                chain(
                    [sorted_snapshots[i]],
                    prune1
                )
            )]

        return

        # Assert that adding an element to the middle of the range yields the same result
        # as pruning would if it had existed the entire time
        for i in range(len(snapshots)-1):
            print()
            print("Prune Late Entry", i)
            prune1 = [item for item in Snapshot.prune(chain(sorted_snapshots[0:i], sorted_snapshots[i+1:]))]
            sorted_prune1_plus_element = list(reversed(sorted(chain(prune1, [sorted_snapshots[i]]), key=lambda snap: snap.timestamp)))
            prune2 = [item for item in Snapshot.prune(sorted_prune1_plus_element)]
            self.assertEqual(pruned, prune2)


        return

        print()
        print("prune_0_6")
        prune_0_6 = [item for item in Snapshot.prune(sorted_snapshots[:len(sorted_snapshots)//2])]
        # [print(s) for s in prune_0_6]

        print()
        print("prune_7_13")
        prune_7_13 = [item for item in Snapshot.prune(sorted_snapshots[len(sorted_snapshots)//2:])]
        # [print(s) for s in prune_7_13]

        print()
        print("prune")
        prune = [item for item in Snapshot.prune(chain(prune_0_6, prune_7_13))]
        # [print(s) for s in prune]

        # self.assertEqual(prune, prune1)
