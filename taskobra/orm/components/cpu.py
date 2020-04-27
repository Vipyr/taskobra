# Libraries
from sqlalchemy import Column, Float, ForeignKey, Integer, String
# Taskobra
from taskobra.orm.components import Component


class CPU(Component):
    __tablename__ = "CPU"
    unique_id = Column(Integer, ForeignKey("Component.unique_id"), primary_key=True)
    manufacturer = Column(String)
    model = Column(String)
    isa = Column(String)
    tdp = Column(Integer)
    core_count = Column(Integer)
    threads_per_core = Column(Integer)
    nominal_frequency = Column(Float)
    maximum_frequency = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
    }

    @property
    def threads(self):
        return self.core_count * self.threads_per_core

    def __repr__(self):
        return f"<CPU({self.manufacturer} {self.model} ({self.core_count}/{self.threads}x{self.nominal_frequency} GHz {self.isa}))>"
