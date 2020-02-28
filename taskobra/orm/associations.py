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
