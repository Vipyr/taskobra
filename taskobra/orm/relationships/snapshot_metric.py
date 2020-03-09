# Libraries
from sqlalchemy import Column, ForeignKey, Integer, Table
# Taskobra
from taskobra.orm.base import ORMBase


snapshot_metric_table = Table(
    "SnapshotMetric", ORMBase.metadata,
    Column("snapshot_id", Integer, ForeignKey("Snapshot.unique_id")),
    Column("metric_id", Integer, ForeignKey("Metric.unique_id")),
)
