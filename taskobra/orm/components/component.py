# Libraries
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
# Taskobra
from taskobra.orm.base import ORMBase


class Component(ORMBase):
    __tablename__ = "Component"
    unique_id = Column(Integer, primary_key=True)
    system_components = relationship("SystemComponent")
    systems = association_proxy("system_components", "system")
    component_type = Column(Enum(
        "CPU",
        "GPU",
        "Memory",
        "OperatingSystem",
        "NetworkAdapter",
        "Storage",
        name="ComponentType"
    ))


    __mapper_args__ = {
        "polymorphic_identity": __tablename__,
        "polymorphic_on": component_type,
    }
