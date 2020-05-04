# Libraries
from sqlalchemy import Column, ForeignKey, Integer, Table
# Taskobra
from taskobra.orm.base import ORMBase


system_snapshot_table = Table(
    "SystemSnapshot", ORMBase.metadata,
    Column("system_id", Integer, ForeignKey("System.unique_id")),
    Column("snapshot_id", Integer, ForeignKey("Snapshot.unique_id")),
)
