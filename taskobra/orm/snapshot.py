# Libraries
from collections import defaultdict
from datetime import timedelta
from functools import reduce
from itertools import chain
from sqlalchemy import DateTime, Column, Float, Integer
from sqlalchemy.orm import relationship
from typing import Iterable
# Taskobra
from taskobra.orm.base import ORMBase
from taskobra.orm.relationships.snapshot_metric import snapshot_metric_table


class Snapshot(ORMBase):
    __tablename__ = "Snapshot"
    unique_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    metrics = relationship("Metric", secondary=snapshot_metric_table)
    sample_count = Column(Integer, default=1)
    sample_rate = Column(Float, default=1.0)
    sample_base = Column(Float, default=2.0)
    sample_exponent = Column(Float, default=0.0)

    @property
    def sample_dt(self):
        return timedelta(seconds=self.sample_rate * self.sample_base ** self.sample_exponent)

    @property
    def t_start(self):
        return self.timestamp - (self.sample_dt / 2)

    @property
    def t_end(self):
        return self.timestamp + (self.sample_dt / 2)

    def covers(self, other: "Snapshot"):
        return self.t_start <= other.timestamp < self.t_end

    def merge(self, other: "Snapshot"):
        """ Merges two adjacent Snapshots together.  Expects self to be
            younger than other
        """
        if self.timestamp < other.timestamp:
            raise ValueError(f"Attempt to merge Snapshots out of order {self}.merge({other})")

        sample_count = self.sample_count + other.sample_count
        sample_rate = (self.sample_rate * self.sample_count + other.sample_rate * other.sample_count) / sample_count
        sample_base = (self.sample_base * self.sample_count + other.sample_base * other.sample_count) / sample_count
        sample_exponent = max(self.sample_exponent, other.sample_exponent)

        # Create the new Snapshot with the time information,
        # and a guess about the exponent.
        metrics_by_type = defaultdict(list)
        [metrics_by_type[type(metric)].append(metric) for metric in self.metrics]
        [metrics_by_type[type(metric)].append(metric) for metric in other.metrics]
        pruned_metrics = []
        [pruned_metrics.extend(metric_type.prune(metrics)) for metric_type, metrics in metrics_by_type.items()]
        merged = Snapshot(
            metrics=pruned_metrics,
            sample_count=sample_count,
            sample_rate=sample_rate,
            sample_base=sample_base,
            sample_exponent=sample_exponent,
        )
        # Compute a weighted average of the timestamps, adjusted by sample count.
        merged.timestamp = other.timestamp + (self.timestamp - other.timestamp) * self.sample_count / merged.sample_count
        # Expand the merged time slice until it covers both Snapshots
        while not (merged.covers(self) and merged.covers(other)):
            merged.sample_exponent += 1
            merged.timestamp = other.timestamp + (self.timestamp - other.timestamp) * self.sample_count / merged.sample_count
        return merged

    @classmethod
    def prune(cls, snapshots: Iterable["Snapshot"]):
        """ Prunes an iterable of Snapshots, yielding new Snapshot instances
            each time a new timeslice is finished off.
            `snapshots` must be sorted by timestamp from youngest to oldest (descending)
        """
        snapshot_iterable = chain(snapshots)
        pruned = next(snapshot_iterable)
        for snapshot in snapshot_iterable:
            if pruned.covers(snapshot):
                pruned = pruned.merge(snapshot)
            else:
                yield pruned
                pruned = snapshot


        return

        snap0 = next(snapshots)
        snapshot_iterable = reversed(
            sorted(
                snapshots,
                key=lambda snapshot: snapshot.timestamp,
            ),
        )
        prunes = []
        snaps = []
        sample_exponent = 1.0
        sample_rate = None
        sample_base = None
        dt = timedelta(seconds=snap0.sample_dt / 2)
        time_slice = (snap0.timestamp - dt, snap0.timestamp + dt)
        for snapshot in snapshot_iterable:
            if time_slice and time_slice[0] > snapshot.timestamp >= time_slice[1]:
                sample_rate = (sample_rate * len(snaps) + snapshot.sample_rate) / (len(snaps) + 1)
                sample_base = (sample_base * len(snaps) + snapshot.sample_base) / (len(snaps) + 1)
                time_slice = (time_slice[0], time_slice[0] - timedelta(seconds=sample_rate * sample_base ** sample_exponent))
            else:
                if snaps:
                    metrics_by_type = defaultdict(list)
                    [
                        [
                            metrics_by_type[type(metric)].append(metric)
                            for metric in snap.metrics
                        ]
                        for snap in snaps
                    ]
                    pruned_metrics = []
                    [pruned_metrics.extend(metric_type.prune(metrics))
                        for metric_type, metrics in metrics_by_type.items()]
                    prunes.append(
                        cls(
                            timestamp=(time_slice[0] + ((time_slice[1] - time_slice[0]) / 2)),
                            metrics=pruned_metrics,
                            sample_rate=sample_rate,
                            sample_base=sample_base,
                            sample_exponent=sample_exponent,
                        )
                    )
                    snaps = []
                sample_exponent += 1
                sample_rate = snapshot.sample_rate
                sample_base = snapshot.sample_base
                time_slice = (time_slice[1], time_slice[1] - timedelta(seconds=sample_rate * sample_base ** sample_exponent))
            snaps.append(snapshot)

        metrics_by_type = defaultdict(list)
        [
            [
                metrics_by_type[type(metric)].append(metric)
                for metric in snapshot.metrics
            ]
            for snapshot in snaps
        ]
        pruned_metrics = []
        [pruned_metrics.extend(metric_type.prune(metric))
            for metric_type, metric in metrics_by_type.items()]
        prunes.append(
            cls(
                timestamp=(time_slice[0] + ((time_slice[1] - time_slice[0]) / 2)),
                metrics=pruned_metrics,
                sample_rate=sample_rate,
                sample_base=sample_base,
                sample_exponent=sample_exponent,
            )
        )
        return prunes

    def __repr__(self):
        total_metrics = sum(metric.sample_count for metric in self.metrics)
        t0 = self.t_start.strftime("%d/%b/%y %H:%M:%S.%f")
        t1 = self.t_end.strftime("%d/%b/%y %H:%M:%S.%f")
        dt = self.sample_rate * self.sample_base ** self.sample_exponent
        return f"<Snapshot({t0} - {t1} : {self.sample_rate:.3}*{self.sample_base:.3}^{self.sample_exponent:.3}({dt:.3}) : {total_metrics})>"

    def __eq__(self, other: "Snapshot"):
        return (
            self.timestamp == other.timestamp and
            self.sample_count == other.sample_count and
            self.sample_base == other.sample_base and
            self.sample_exponent == other.sample_exponent and
            self.sample_rate == other.sample_rate and
            reduce(
                lambda x, y: x and y,
                (self_metric == other_metric for self_metric, other_metric in zip(self.metrics, other.metrics)),
                True
            )
        )
