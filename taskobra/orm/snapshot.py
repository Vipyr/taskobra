# Libraries
from collections import defaultdict
from datetime import datetime, timedelta
from functools import reduce
from itertools import chain
from math import ceil, log
from sqlalchemy import DateTime, Column, Float, Integer
from sqlalchemy.orm import relationship
from typing import Generator
from typing import Iterable
# Taskobra
from taskobra.orm.base import ORMBase
from taskobra.orm.relationships.snapshot_metric import snapshot_metric_table
from taskobra.orm.relationships.system_snapshot import system_snapshot_table

class Snapshot(ORMBase):

    class UnmergableException(Exception): pass

    __tablename__ = "Snapshot"
    unique_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    system = relationship("System", secondary=system_snapshot_table)
    metrics = relationship("Metric", secondary=snapshot_metric_table, lazy="joined")
    sample_count = Column(Integer, default=1)
    sample_rate = Column(Float, default=1.0)
    sample_base = Column(Float, default=2.0)
    sample_exponent = Column(Integer, default=0)

    @staticmethod
    def dt(rate, base, exponent):
        return timedelta(seconds=rate * base ** exponent)

    @property
    def sample_dt(self):
        return Snapshot.dt(self.sample_rate, self.sample_base, self.sample_exponent)

    @property
    def t_start(self):
        return self.timestamp - self.sample_dt

    @property
    def t_end(self):
        return self.timestamp

    def overlaps(self, other: "Snapshot"):
        return (
            self.timestamp and
            other.timestamp and
            (
                self.t_start  < other.timestamp <= self.t_end or
                other.t_start < self.timestamp  <= other.t_end
            )
        )

    def merge(self, other: "Snapshot"):
        """ Merges two Snapshots together.
        associative
        commutative
        identity
        """
        if self.overlaps(other):
            sample_count = self.sample_count + other.sample_count
            sample_rate = (self.sample_rate * self.sample_count + other.sample_rate * other.sample_count) / sample_count
            sample_base = (self.sample_base * self.sample_count + other.sample_base * other.sample_count) / sample_count

            # Create the new Snapshot
            metrics_by_type = defaultdict(list)
            [metrics_by_type[type(metric)].append(metric) for metric in self.metrics]
            [metrics_by_type[type(metric)].append(metric) for metric in other.metrics]
            pruned_metrics = []
            [pruned_metrics.extend(metric_type.prune(metrics)) for metric_type, metrics in metrics_by_type.items()]
            merged = Snapshot(
                metrics=pruned_metrics,
                timestamp=max(self.timestamp, other.timestamp),
                sample_count=sample_count,
                sample_rate=sample_rate,
                sample_base=sample_base,
                sample_exponent=max(self.sample_exponent, other.sample_exponent),
            )
            return merged
        else:
            raise Snapshot.UnmergableException()

    @staticmethod
    def format_snap(snap):
        return f"({snap.t_start.second:0>2}-{snap.t_end.second:0>2} {snap.sample_exponent} {snap.sample_count})"

    @classmethod
    def prune(cls, snapshots: Iterable["Snapshot"]):
        """ Prunes an iterable of Snapshots, yielding new Snapshot instances
            each time a new timeslice is finished off.
            `snapshots` must be sorted by timestamp from youngest to oldest (descending)
        """
        if not isinstance(snapshots, Generator):
            snapshots = chain(snapshots)

        pruned = Snapshot(sample_count=0, sample_exponent=1)

        for snapshot in snapshots:
            try:
                pruned = pruned.merge(snapshot)
                yield snapshot, None
            except Snapshot.UnmergableException:
                if pruned.sample_count:
                    yield snapshot, pruned
                else:
                    yield snapshot, None
                pruned = Snapshot(
                    timestamp=snapshot.timestamp,
                    sample_count=snapshot.sample_count,
                    sample_rate=snapshot.sample_rate,
                    sample_base=snapshot.sample_base,
                    sample_exponent=pruned.sample_exponent + 1,
                    metrics=snapshot.metrics,
                )
        if pruned.sample_count:
            yield None, pruned

    def __repr__(self):
        total_metrics = sum(metric.sample_count for metric in self.metrics)
        ts = f"{self.timestamp.strftime('%d/%b/%y %H:%M:%S')}.{self.timestamp.microsecond // 10000}" if self.timestamp else "--:--:--.-"
        dt = self.sample_rate * self.sample_base ** self.sample_exponent
        return f"<Snapshot({ts} : {self.sample_rate:.3}*{self.sample_base:.3}^{self.sample_exponent}({dt:.3}) : {total_metrics})>"

    def __eq__(self, other: "Snapshot"):
        return (
            self.timestamp == other.timestamp and
            self.sample_count == other.sample_count and
            self.sample_base == other.sample_base and
            self.sample_exponent == other.sample_exponent and
            self.sample_rate == other.sample_rate and
            len(self.metrics) == len(other.metrics) and
            reduce(
                lambda x, y: x and y,
                (self_metric == other_metric for self_metric, other_metric in zip(self.metrics, other.metrics)),
                True
            )
        )
