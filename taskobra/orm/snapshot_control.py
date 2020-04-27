# Libraries
from datetime import timedelta
from sqlalchemy import Column, DateTime, Float, Integer
# Taskobra
from taskobra.orm.base import ORMBase


class SnapshotControl(ORMBase):
    __tablename__ = "SnapshotControl"
    unique_id = Column(Integer, primary_key=True)
    pruning_delay = Column(Float, default=0.0)
    max_prune_time_slice = Column(Float, default=0.0)
    default_sample_base = Column(Float, default=10.0)
    default_sample_rate = Column(Float, default=1.0)
    timestamp = Column(DateTime)

    @property
    def max_prune_timedelta(self):
        return timedelta(seconds=self.max_prune_time_slice)
