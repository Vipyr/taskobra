# Libraries
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
# Taskobra
from taskobra.orm.base import ORMBase


class SystemComponent(ORMBase):
    __tablename__ = "SystemComponent"
    system_id = Column(Integer, ForeignKey("System.unique_id"), primary_key=True)
    component_id = Column(Integer, ForeignKey("Component.unique_id"), primary_key=True)
    count = Column(Integer, default=1)

    _system = relationship("System")
    _component = relationship("Component")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "count" not in kwargs:
            self.count = 1

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, component: "taskobra.orm.Component"):
        del self.component
        self._component = component
        self._component.system_components.append(self)

    @component.deleter
    def component(self):
        if self._component:
            self._component.system_components.remove(self)
            del self._component

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system: "taskobra.orm.System"):
        del self.system
        self._system = system
        self._system.system_components.append(self)

    @system.deleter
    def system(self):
        if self._system:
            self._system.system_components.remove(self)
            del self._system

    def __repr__(self):
        return f"<SystemComponent({self.system.name}: {self.component})>"
