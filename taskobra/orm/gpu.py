# Libraries
from sqlalchemy import Column, Float, ForeignKey, Integer, String
# Taskobra
from .component import Component


class GPU(Component):
    __tablename__ = "GPU"
    unique_id = Column(Integer, ForeignKey("Component.unique_id"), primary_key=True)
    manufacturer = Column(String)
    model = Column(String)
    architecture = Column(String)
    tdp = Column(Integer)
    core_count = Column(Integer)
    memory = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
    }

    def __repr__(self):
        return f"<GPU({self.manufacturer} {self.model} ({self.architecture}))>"
