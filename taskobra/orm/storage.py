# Libraries
from sqlalchemy import Column, Float, ForeignKey, Integer, String
# Taskobra
from taskobra.orm.component import Component


class Storage(Component):
    __tablename__ = "Storage"
    unique_id = Column(Integer, ForeignKey("Component.unique_id"), primary_key=True)
    manufacturer = Column(String)
    model = Column(String)
    standard = Column(String)
    capacity = Column(Float)
    max_read = Column(Float)
    max_write = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
    }

    def __repr__(self):
        return f"<Storage({self.manufacturer} {self.model})>"
