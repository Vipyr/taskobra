# Libraries
from sqlalchemy import Column, Float, ForeignKey, Integer, String
# Taskobra
from .component import Component


class CPU(Component):
    __tablename__ = "CPU"
    unique_id = Column(Integer, ForeignKey("Component.unique_id"), primary_key=True)
    manufacturer = Column(String)
    model = Column(String)
    isa = Column(String)
    tdp = Column(Integer)
    core_count = Column(Integer)
    threads_per_core = Column(Integer)
    minimum_frequency = Column(Float)
    maximum_frequency = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
    }

    def __repr__(self):
        return f"<CPU({self.manufacturer} {self.model} ({self.isa}))>"
