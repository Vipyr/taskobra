# Libraries
from sqlalchemy import Column, Float, ForeignKey, Integer, String
# Taskobra
from taskobra.orm.component import Component


class OperatingSystem(Component):
    __tablename__ = "OperatingSystem"
    unique_id = Column(Integer, ForeignKey("Component.unique_id"), primary_key=True)
    developer = Column(String)
    name = Column(String)
    version = Column(String)
    build = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
    }

    def __repr__(self):
        return f"<OperatingSystem({self.developer} {self.name})>"
