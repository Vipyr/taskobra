# Libraries
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
# Taskobra
from .base import ORMBase


user_role_table = Table(
    "UserRole", ORMBase.metadata,
    Column("user_id", Integer, ForeignKey("User.unique_id")),
    Column("role_id", Integer, ForeignKey("Role.unique_id")),
)


class UserSystemRole(ORMBase):
    __tablename__ = "UserSystemRole"
    user_id = Column(Integer, ForeignKey("User.unique_id"), primary_key=True)
    system_id = Column(Integer, ForeignKey("System.unique_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("Role.unique_id"), primary_key=True)

    user = relationship("User")
    system = relationship("System")
    role = relationship("Role")

    def __setattr__(self, attr, value):
        if attr == "user" and self not in value.system_roles:
            if self.user:
                self.user.system_roles.remove(self)
            value.system_roles.append(self)
        elif attr == "system" and self not in value.user_roles:
            if self.system:
                self.system.user_roles.remove(self)
            value.user_roles.append(self)
        super().__setattr__(attr, value)

    def __repr__(self):
        return f"<UserSystemRole({self.user.name}, {self.system.name}, {self.role.name})>"


# system_component_table = Table(
#     "SystemComponent", ORMBase.metadata,
#     Column("system_id", Integer, ForeignKey("System.unique_id")),
#     Column("component_id", Integer, ForeignKey("Component.unique_id")),
# )


class SystemComponent(ORMBase):
    __tablename__ = "SystemComponent"
    system_id = Column(Integer, ForeignKey("System.unique_id"), primary_key=True)
    component_id = Column(Integer, ForeignKey("Component.unique_id"), primary_key=True)
    count = Column(Integer, default=1)

    system = relationship("System")
    component = relationship("Component")

    def __setattr__(self, attr, value):
        if attr == "component" and self not in value.system_components:
            if self.component:
                self.component.system_components.remove(self)
            value.system_components.append(self)
        elif attr == "system" and self not in value.system_components:
            if self.system:
                self.system.system_components.remove(self)
            value.system_components.append(self)
        super().__setattr__(attr, value)

    def __repr__(self):
        return f"<SystemComponent({self.system.name}: {self.component})>"
