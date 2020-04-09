# Libraries
from collections import defaultdict
from datetime import timedelta
from functools import reduce
from itertools import chain
from math import log
from sqlalchemy import DateTime, Column, Float, Integer
from sqlalchemy.orm import relationship
from typing import Generator
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
        """ Merges two Snapshots together.
        """
        younger, older = sorted((self, other), key=lambda snap: snap.timestamp)

        sample_count = younger.sample_count + older.sample_count
        sample_rate = (younger.sample_rate * younger.sample_count + older.sample_rate * older.sample_count) / sample_count
        sample_base = (younger.sample_base * younger.sample_count + older.sample_base * older.sample_count) / sample_count
        # sample_exponent = max(younger.sample_exponent, older.sample_exponent)
        t_start = min(younger.t_start, older.t_start)
        t_end = max(younger.t_end, older.t_end)
        sample_dt = t_end - t_start
        timestamp = t_start + sample_dt / 2
        sample_exponent = log(sample_dt.total_seconds(), sample_base)

        # Create the new Snapshot with the time information,
        # and a guess about the exponent.
        metrics_by_type = defaultdict(list)
        [metrics_by_type[type(metric)].append(metric) for metric in younger.metrics]
        [metrics_by_type[type(metric)].append(metric) for metric in older.metrics]
        pruned_metrics = []
        [pruned_metrics.extend(metric_type.prune(metrics)) for metric_type, metrics in metrics_by_type.items()]
        merged = Snapshot(
            metrics=pruned_metrics,
            timestamp=timestamp,
            sample_count=sample_count,
            sample_rate=sample_rate,
            sample_base=sample_base,
            sample_exponent=sample_exponent,
        )
        # # Compute a new timestamp
        # merged.timestamp = older.timestamp + (younger.timestamp - older.timestamp) * younger.sample_count / merged.sample_count
        # # Expand the merged time slice until it covers both Snapshots
        # while not (merged.covers(younger) and merged.covers(older)):
        #     merged.sample_exponent += 1
        #     merged.timestamp = older.timestamp + (younger.timestamp - older.timestamp) * younger.sample_count / merged.sample_count
        return merged

    @classmethod
    def prune(cls, snapshots: Iterable["Snapshot"]):
        """ Prunes an iterable of Snapshots, yielding new Snapshot instances
            each time a new timeslice is finished off.
            `snapshots` must be sorted by timestamp from youngest to oldest (descending)
        """
        if not isinstance(snapshots, Generator):
            snapshots = chain(snapshots)
        pruned = next(snapshots)

        # Base the time slices on only t_end, going
        # backwards in time by using the rate/base
        # and starting with an exponent of 1.0.
        # Collect up and merge all snapshots
        # that fall in that window, then increment
        # the exponent and move on to the t_start
        # of the previous range.  Do this until
        # we run out of data to consume.
        t_end = pruned.t_end

        for snapshot in snapshots:
            if pruned.covers(snapshot):
                pruned = pruned.merge(snapshot)
            else:
                yield pruned
                pruned = snapshot


        return

        snap0 = next(snapshots)
        snapshots = reversed(
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
        for snapshot in snapshots:
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
        t0 = self.t_start
        t1 = self.t_end
        t0s = f"{t0.strftime('%d/%b/%y %H:%M:%S')}.{t0.microsecond // 10000}"
        t1s = f"{t1.strftime('%d/%b/%y %H:%M:%S')}.{t1.microsecond // 10000}"
        dt = self.sample_rate * self.sample_base ** self.sample_exponent
        return f"<Snapshot({t0s} - {t1s} : {self.sample_rate:.3}*{self.sample_base:.3}^{self.sample_exponent:.3}({dt:.3}) : {total_metrics})>"

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
