# Libraries
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
# Taskobra
from taskobra.orm.base import ORMBase
from taskobra.orm.relationships import SystemComponent, system_snapshot_table


class System(ORMBase):
    __tablename__ = "System"
    unique_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_roles = relationship("UserSystemRole")
    system_components = relationship("SystemComponent")
    snapshots = relationship("Snapshot", back_populates="system", order_by="desc(Snapshot.timestamp)")

    @property
    def components(self):
        for system_component in self.system_components:
            for _ in range(system_component.count):
                yield system_component.count, system_component.component

    def add_component(self, component):
        for system_component in self.system_components:
            if system_component.component is component:
                system_component.count += 1
                return
        SystemComponent(system=self, component=component, count=1)

    def __repr__(self):
        components = [
            f"{count}x{repr(component)}"
            for count, component in self.components
        ]
        return f"<System(name={self.name}, {components}, unique_id={self.unique_id})>"

    def __str__(self):
        linesep = "\n    "
        components = [
            f"{linesep}{repr(component)}"
            for _, component in self.components
        ]
        return f"{self.name}:{''.join(components)}"
