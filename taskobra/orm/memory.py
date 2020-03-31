# Libraries
from sqlalchemy import Column, Float, ForeignKey, Integer, String
# Taskobra
from .component import Component


class Memory(Component):
    __tablename__ = "Memory"
    unique_id = Column(Integer, ForeignKey("Component.unique_id"), primary_key=True)
    manufacturer = Column(String)
    model = Column(String)
    standard = Column(String)
    capacity = Column(Float)
    frequency = Column(Float)
    cas_latency = Column(Integer)
    t_rcd = Column(Integer)
    t_rp = Column(Integer)
    t_ras = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
    }

    def __repr__(self):
        return f"<Memory({self.manufacturer} {self.model} ({self.capacity} GB {self.standard} {self.cas_latency}-{self.t_rcd}-{self.t_rp}-{self.t_ras}))>"
