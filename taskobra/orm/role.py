# Libraries
from sqlalchemy import Column, Integer, String
# Taskobra
from .base import ORMBase


class Role(ORMBase):
    __tablename__ = "Role"
    unique_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Role(name={self.name}, unique_id={self.unique_id})>"
