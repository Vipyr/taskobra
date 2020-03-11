# Libraries
from collections import defaultdict
from datetime import timedelta
from functools import reduce
from sqlalchemy import DateTime, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from statistics import mean
from typing import Collection
# Taskobra
from taskobra.orm.base import ORMBase
from taskobra.orm.relationships.snapshot_metric import snapshot_metric_table

class Snapshot(ORMBase):
    __tablename__ = "Snapshot"
    unique_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    metrics = relationship("Metric", secondary=snapshot_metric_table)
    sample_rate = Column(Float, default=1.0)
    sample_base = Column(Float, default=2.0)
    sample_exponent = Column(Float, default=0.0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "sample_rate" not in kwargs:
            self.sample_rate = type(self).sample_rate.default.arg
        if "sample_base" not in kwargs:
            self.sample_base = type(self).sample_base.default.arg
        if "sample_exponent" not in kwargs:
            self.sample_exponent = type(self).sample_exponent.default.arg

    @classmethod
    def prune(cls, t0, snapshots: Collection["Snapshot"]):
        snap0 = reduce(lambda x, y: y if y.timestamp > x.timestamp else x, filter(lambda x: x.timestamp <= t0, snapshots))
        print(f"snap0 = {snap0}")
        snapshot_iterable = reversed(
            sorted(
                filter(
                    lambda snapshot: snapshot.timestamp <= t0,
                    snapshots,
                ),
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

    @property
    def sample_dt(self):
        return self.sample_rate * self.sample_base ** self.sample_exponent

    def __repr__(self):
        total_metrics = sum(metric.sample_count for metric in self.metrics)
        dt = timedelta(seconds=self.sample_dt / 2)
        t0 = (self.timestamp - dt).strftime("%d/%b/%y %H:%M:%S")
        t1 = (self.timestamp + dt).strftime("%d/%b/%y %H:%M:%S")
        return f"<Snapshot({t0} - {t1} : {self.sample_rate:.3}*{self.sample_base:.3}^{self.sample_exponent:.3}({self.sample_dt:.3}) : {total_metrics})>"
